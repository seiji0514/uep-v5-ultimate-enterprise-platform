"""
ESGレポートサービス
"""

from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, datetime
from app.models.esg import ESGReport, CarbonFootprint
from app.core.influxdb_client import query_time_series_data
from loguru import logger
import pandas as pd


class ESGService:
    """ESGレポートサービス"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_esg_reports(
        self,
        report_type: Optional[str] = None,
        period_start: Optional[date] = None,
        period_end: Optional[date] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[dict]:
        """ESGレポート一覧の取得"""
        query = self.db.query(ESGReport)
        
        if report_type:
            query = query.filter(ESGReport.report_type == report_type)
        if period_start:
            query = query.filter(ESGReport.period_start >= period_start)
        if period_end:
            query = query.filter(ESGReport.period_end <= period_end)
        
        reports = query.offset(skip).limit(limit).all()
        return [{
            "id": str(report.id),
            "report_name": report.report_name,
            "report_type": report.report_type,
            "period_start": report.period_start.isoformat(),
            "period_end": report.period_end.isoformat(),
            "status": report.status,
            "file_path": report.file_path,
            "created_at": report.created_at.isoformat()
        } for report in reports]
    
    def generate_esg_report(
        self,
        report_type: str,
        period_start: date,
        period_end: date
    ) -> dict:
        """ESGレポートの自動生成"""
        try:
            # 環境データの取得
            start_time = datetime.combine(period_start, datetime.min.time())
            end_time = datetime.combine(period_end, datetime.max.time())
            
            # 環境データの集計
            env_data = query_time_series_data(
                measurement="environment_data",
                start=start_time.isoformat(),
                stop=end_time.isoformat()
            )
            
            # エネルギーデータの集計
            energy_data = query_time_series_data(
                measurement="energy_data",
                start=start_time.isoformat(),
                stop=end_time.isoformat()
            )
            
            # レポートデータの生成
            report_data = {
                "report_type": report_type,
                "period_start": period_start.isoformat(),
                "period_end": period_end.isoformat(),
                "environment": {
                    "data_points": len(env_data),
                    "summary": self._summarize_environment_data(env_data)
                },
                "energy": {
                    "data_points": len(energy_data),
                    "summary": self._summarize_energy_data(energy_data)
                }
            }
            
            # レポートの保存
            report = ESGReport(
                report_name=f"ESG Report {report_type} {period_start} to {period_end}",
                report_type=report_type,
                period_start=period_start,
                period_end=period_end,
                status="generated",
                metadata=report_data
            )
            
            self.db.add(report)
            self.db.commit()
            self.db.refresh(report)
            
            logger.info(f"ESGレポート生成成功: report_type={report_type}")
            return {
                "id": str(report.id),
                "report_name": report.report_name,
                "status": report.status,
                "data": report_data
            }
            
        except Exception as e:
            logger.error(f"ESGレポート生成エラー: {e}")
            raise
    
    def _summarize_environment_data(self, data: List[dict]) -> dict:
        """環境データの要約"""
        if not data:
            return {}
        
        values = [d.get("value", 0) for d in data if "value" in d]
        if not values:
            return {}
        
        return {
            "count": len(values),
            "mean": sum(values) / len(values),
            "min": min(values),
            "max": max(values)
        }
    
    def _summarize_energy_data(self, data: List[dict]) -> dict:
        """エネルギーデータの要約"""
        if not data:
            return {}
        
        consumption = [d.get("consumption", 0) for d in data if "consumption" in d]
        generation = [d.get("generation", 0) for d in data if "generation" in d]
        
        return {
            "total_consumption": sum(consumption),
            "total_generation": sum(generation),
            "balance": sum(generation) - sum(consumption)
        }
    
    def get_carbon_footprint(
        self,
        period_start: Optional[date] = None,
        period_end: Optional[date] = None,
        scope: Optional[str] = None
    ) -> List[dict]:
        """カーボンフットプリントの取得"""
        query = self.db.query(CarbonFootprint)
        
        if period_start:
            query = query.filter(CarbonFootprint.period_start >= period_start)
        if period_end:
            query = query.filter(CarbonFootprint.period_end <= period_end)
        if scope:
            query = query.filter(CarbonFootprint.scope == scope)
        
        carbon_footprints = query.all()
        return [{
            "id": str(cf.id),
            "period_start": cf.period_start.isoformat(),
            "period_end": cf.period_end.isoformat(),
            "scope": cf.scope,
            "category": cf.category,
            "value": float(cf.value),
            "unit": cf.unit
        } for cf in carbon_footprints]
    
    def create_carbon_footprint(
        self,
        period_start: date,
        period_end: date,
        scope: str,
        category: str,
        value: float,
        unit: str = "tCO2e"
    ) -> dict:
        """カーボンフットプリントの作成"""
        try:
            carbon_footprint = CarbonFootprint(
                period_start=period_start,
                period_end=period_end,
                scope=scope,
                category=category,
                value=value,
                unit=unit
            )
            
            self.db.add(carbon_footprint)
            self.db.commit()
            self.db.refresh(carbon_footprint)
            
            logger.info(f"カーボンフットプリント作成成功: scope={scope}, category={category}, value={value}")
            return {
                "id": str(carbon_footprint.id),
                "message": "カーボンフットプリントを作成しました"
            }
            
        except Exception as e:
            logger.error(f"カーボンフットプリント作成エラー: {e}")
            raise

