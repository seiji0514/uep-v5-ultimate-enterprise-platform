package com.healthcare.monitoring;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.netflix.eureka.EnableEurekaClient;
import org.springframework.kafka.annotation.EnableKafka;
import org.springframework.web.bind.annotation.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.http.HttpStatus;
import org.springframework.web.servlet.mvc.method.annotation.SseEmitter;

import java.time.LocalDateTime;
import java.util.*;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;

/**
 * AI統合ヘルスケアプラットフォーム - Realtime Monitoring Service
 * 
 * テクニカルアーキテクトレベルの実装例：
 * - リアルタイムストリーミング
 * - WebSocket・Server-Sent Events
 * - 異常検知・アラート
 * - 高可用性・低レイテンシ
 * 
 * @author OGAWA SEIJI
 * @version 1.0.0
 */
@SpringBootApplication
@EnableEurekaClient
@EnableKafka
@RestController
@RequestMapping("/api/v1/monitoring")
public class RealtimeMonitoringService {

    @Autowired
    private VitalSignsStreamProcessor streamProcessor;
    
    @Autowired
    private AlertManager alertManager;
    
    @Autowired
    private MonitoringEventPublisher eventPublisher;
    
    @Autowired
    private HealthDataAggregator dataAggregator;

    // リアルタイム接続管理
    private final Map<String, SseEmitter> activeConnections = new ConcurrentHashMap<>();
    private final ScheduledExecutorService scheduler = Executors.newScheduledThreadPool(10);

    public static void main(String[] args) {
        SpringApplication.run(RealtimeMonitoringService.class, args);
    }

    /**
     * リアルタイムバイタル監視ストリーム
     * テクニカルアーキテクトレベル：Server-Sent Events・リアルタイムストリーミング
     */
    @GetMapping("/vitals/stream/{patientId}")
    public SseEmitter streamVitalSigns(@PathVariable String patientId) {
        SseEmitter emitter = new SseEmitter(Long.MAX_VALUE);
        String connectionId = UUID.randomUUID().toString();
        
        activeConnections.put(connectionId, emitter);
        
        // 接続終了時のクリーンアップ
        emitter.onCompletion(() -> activeConnections.remove(connectionId));
        emitter.onTimeout(() -> activeConnections.remove(connectionId));
        emitter.onError((ex) -> activeConnections.remove(connectionId));
        
        // リアルタイムストリーミング開始
        startVitalSignsStreaming(patientId, emitter, connectionId);
        
        return emitter;
    }

    /**
     * 患者リスト監視ダッシュボード
     * テクニカルアーキテクトレベル：リアルタイム集計・可視化
     */
    @GetMapping("/dashboard/patients")
    public ResponseEntity<Map<String, Object>> getPatientMonitoringDashboard() {
        try {
            CompletableFuture<PatientMonitoringSummary> futureSummary = 
                dataAggregator.getPatientMonitoringSummary();
            PatientMonitoringSummary summary = futureSummary.get(500, TimeUnit.MILLISECONDS);
            
            Map<String, Object> response = new HashMap<>();
            response.put("timestamp", LocalDateTime.now());
            response.put("totalPatients", summary.getTotalPatients());
            response.put("activePatients", summary.getActivePatients());
            response.put("criticalPatients", summary.getCriticalPatients());
            response.put("alertsCount", summary.getAlertsCount());
            response.put("patientStatus", summary.getPatientStatus());
            response.put("vitalTrends", summary.getVitalTrends());
            response.put("anomalyDetections", summary.getAnomalyDetections());
            
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE)
                .body(Map.of("error", "Dashboard data temporarily unavailable"));
        }
    }

    /**
     * 異常検知アラート取得
     * テクニカルアーキテクトレベル：リアルタイムアラート・優先度管理
     */
    @GetMapping("/alerts")
    public ResponseEntity<Map<String, Object>> getActiveAlerts(
            @RequestParam(defaultValue = "ALL") String severity,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size) {
        try {
            CompletableFuture<AlertSummary> futureAlerts = 
                alertManager.getActiveAlerts(severity, page, size);
            AlertSummary alerts = futureAlerts.get(200, TimeUnit.MILLISECONDS);
            
            Map<String, Object> response = new HashMap<>();
            response.put("timestamp", LocalDateTime.now());
            response.put("alerts", alerts.getAlerts());
            response.put("totalCount", alerts.getTotalCount());
            response.put("page", page);
            response.put("size", size);
            response.put("severityFilter", severity);
            
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(Map.of("error", "Alert retrieval failed: " + e.getMessage()));
        }
    }

    /**
     * アラート確認・対応
     * テクニカルアーキテクトレベル：ワークフロー管理・状態追跡
     */
    @PostMapping("/alerts/{alertId}/acknowledge")
    public ResponseEntity<Map<String, Object>> acknowledgeAlert(
            @PathVariable String alertId,
            @RequestBody AlertAcknowledgment acknowledgment) {
        try {
            CompletableFuture<AlertStatus> futureStatus = 
                alertManager.acknowledgeAlert(alertId, acknowledgment);
            AlertStatus status = futureStatus.get(100, TimeUnit.MILLISECONDS);
            
            Map<String, Object> response = new HashMap<>();
            response.put("alertId", alertId);
            response.put("status", status.getStatus());
            response.put("acknowledgedBy", acknowledgment.getAcknowledgedBy());
            response.put("acknowledgedAt", LocalDateTime.now());
            response.put("notes", acknowledgment.getNotes());
            
            // アラート対応をイベントとして発行
            eventPublisher.publishAlertAcknowledgment(alertId, acknowledgment);
            
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(Map.of("error", "Alert acknowledgment failed: " + e.getMessage()));
        }
    }

    /**
     * バイタルサイン履歴取得
     * テクニカルアーキテクトレベル：時系列データ・集約分析
     */
    @GetMapping("/vitals/history/{patientId}")
    public ResponseEntity<Map<String, Object>> getVitalSignsHistory(
            @PathVariable String patientId,
            @RequestParam String startTime,
            @RequestParam String endTime,
            @RequestParam(defaultValue = "1m") String interval) {
        try {
            CompletableFuture<VitalSignsHistory> futureHistory = 
                dataAggregator.getVitalSignsHistory(patientId, startTime, endTime, interval);
            VitalSignsHistory history = futureHistory.get(1, TimeUnit.SECONDS);
            
            Map<String, Object> response = new HashMap<>();
            response.put("patientId", patientId);
            response.put("startTime", startTime);
            response.put("endTime", endTime);
            response.put("interval", interval);
            response.put("dataPoints", history.getDataPoints());
            response.put("statistics", history.getStatistics());
            response.put("anomalies", history.getAnomalies());
            
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(Map.of("error", "Vital signs history retrieval failed: " + e.getMessage()));
        }
    }

    /**
     * 予測アラート設定
     * テクニカルアーキテクトレベル：予測分析・プロアクティブ監視
     */
    @PostMapping("/predictive-alerts")
    public ResponseEntity<Map<String, Object>> setPredictiveAlert(
            @RequestBody PredictiveAlertRequest request) {
        try {
            CompletableFuture<PredictiveAlert> futureAlert = 
                alertManager.createPredictiveAlert(request);
            PredictiveAlert alert = futureAlert.get(500, TimeUnit.MILLISECONDS);
            
            Map<String, Object> response = new HashMap<>();
            response.put("alertId", alert.getAlertId());
            response.put("patientId", request.getPatientId());
            response.put("predictionType", request.getPredictionType());
            response.put("threshold", request.getThreshold());
            response.put("timeHorizon", request.getTimeHorizon());
            response.put("status", "ACTIVE");
            response.put("createdAt", LocalDateTime.now());
            
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(Map.of("error", "Predictive alert creation failed: " + e.getMessage()));
        }
    }

    /**
     * リアルタイムストリーミング開始
     */
    private void startVitalSignsStreaming(String patientId, SseEmitter emitter, String connectionId) {
        scheduler.scheduleAtFixedRate(() -> {
            try {
                CompletableFuture<VitalSignsData> futureData = 
                    streamProcessor.getLatestVitalSigns(patientId);
                VitalSignsData data = futureData.get(50, TimeUnit.MILLISECONDS);
                
                Map<String, Object> event = new HashMap<>();
                event.put("timestamp", LocalDateTime.now());
                event.put("patientId", patientId);
                event.put("vitalSigns", data.getVitalSigns());
                event.put("anomalyDetected", data.isAnomalyDetected());
                event.put("riskLevel", data.getRiskLevel());
                
                emitter.send(SseEmitter.event()
                    .name("vital-signs")
                    .data(event));
                
            } catch (Exception e) {
                emitter.completeWithError(e);
                activeConnections.remove(connectionId);
            }
        }, 0, 1, TimeUnit.SECONDS);
    }
}

/**
 * 患者監視サマリー
 */
class PatientMonitoringSummary {
    private int totalPatients;
    private int activePatients;
    private int criticalPatients;
    private int alertsCount;
    private Map<String, Integer> patientStatus;
    private Map<String, Object> vitalTrends;
    private List<AnomalyDetection> anomalyDetections;
    
    // Getters and setters
    public int getTotalPatients() { return totalPatients; }
    public void setTotalPatients(int totalPatients) { this.totalPatients = totalPatients; }
    public int getActivePatients() { return activePatients; }
    public void setActivePatients(int activePatients) { this.activePatients = activePatients; }
    public int getCriticalPatients() { return criticalPatients; }
    public void setCriticalPatients(int criticalPatients) { this.criticalPatients = criticalPatients; }
    public int getAlertsCount() { return alertsCount; }
    public void setAlertsCount(int alertsCount) { this.alertsCount = alertsCount; }
    public Map<String, Integer> getPatientStatus() { return patientStatus; }
    public void setPatientStatus(Map<String, Integer> patientStatus) { this.patientStatus = patientStatus; }
    public Map<String, Object> getVitalTrends() { return vitalTrends; }
    public void setVitalTrends(Map<String, Object> vitalTrends) { this.vitalTrends = vitalTrends; }
    public List<AnomalyDetection> getAnomalyDetections() { return anomalyDetections; }
    public void setAnomalyDetections(List<AnomalyDetection> anomalyDetections) { this.anomalyDetections = anomalyDetections; }
}

/**
 * アラートサマリー
 */
class AlertSummary {
    private List<Alert> alerts;
    private long totalCount;
    
    // Getters and setters
    public List<Alert> getAlerts() { return alerts; }
    public void setAlerts(List<Alert> alerts) { this.alerts = alerts; }
    public long getTotalCount() { return totalCount; }
    public void setTotalCount(long totalCount) { this.totalCount = totalCount; }
}

/**
 * アラート
 */
class Alert {
    private String alertId;
    private String patientId;
    private String alertType;
    private String severity;
    private String message;
    private LocalDateTime timestamp;
    private String status;
    
    // Getters and setters
    public String getAlertId() { return alertId; }
    public void setAlertId(String alertId) { this.alertId = alertId; }
    public String getPatientId() { return patientId; }
    public void setPatientId(String patientId) { this.patientId = patientId; }
    public String getAlertType() { return alertType; }
    public void setAlertType(String alertType) { this.alertType = alertType; }
    public String getSeverity() { return severity; }
    public void setSeverity(String severity) { this.severity = severity; }
    public String getMessage() { return message; }
    public void setMessage(String message) { this.message = message; }
    public LocalDateTime getTimestamp() { return timestamp; }
    public void setTimestamp(LocalDateTime timestamp) { this.timestamp = timestamp; }
    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }
}

/**
 * アラート確認
 */
class AlertAcknowledgment {
    private String acknowledgedBy;
    private String notes;
    private String action;
    
    // Getters and setters
    public String getAcknowledgedBy() { return acknowledgedBy; }
    public void setAcknowledgedBy(String acknowledgedBy) { this.acknowledgedBy = acknowledgedBy; }
    public String getNotes() { return notes; }
    public void setNotes(String notes) { this.notes = notes; }
    public String getAction() { return action; }
    public void setAction(String action) { this.action = action; }
}

/**
 * アラートステータス
 */
class AlertStatus {
    private String status;
    private LocalDateTime updatedAt;
    
    // Getters and setters
    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }
    public LocalDateTime getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(LocalDateTime updatedAt) { this.updatedAt = updatedAt; }
}

/**
 * バイタルサイン履歴
 */
class VitalSignsHistory {
    private List<VitalSignsDataPoint> dataPoints;
    private Map<String, Object> statistics;
    private List<AnomalyDetection> anomalies;
    
    // Getters and setters
    public List<VitalSignsDataPoint> getDataPoints() { return dataPoints; }
    public void setDataPoints(List<VitalSignsDataPoint> dataPoints) { this.dataPoints = dataPoints; }
    public Map<String, Object> getStatistics() { return statistics; }
    public void setStatistics(Map<String, Object> statistics) { this.statistics = statistics; }
    public List<AnomalyDetection> getAnomalies() { return anomalies; }
    public void setAnomalies(List<AnomalyDetection> anomalies) { this.anomalies = anomalies; }
}

/**
 * バイタルサインデータポイント
 */
class VitalSignsDataPoint {
    private LocalDateTime timestamp;
    private Map<String, Double> vitalSigns;
    private boolean anomalyDetected;
    
    // Getters and setters
    public LocalDateTime getTimestamp() { return timestamp; }
    public void setTimestamp(LocalDateTime timestamp) { this.timestamp = timestamp; }
    public Map<String, Double> getVitalSigns() { return vitalSigns; }
    public void setVitalSigns(Map<String, Double> vitalSigns) { this.vitalSigns = vitalSigns; }
    public boolean isAnomalyDetected() { return anomalyDetected; }
    public void setAnomalyDetected(boolean anomalyDetected) { this.anomalyDetected = anomalyDetected; }
}

/**
 * 予測アラートリクエスト
 */
class PredictiveAlertRequest {
    private String patientId;
    private String predictionType;
    private double threshold;
    private String timeHorizon;
    private Map<String, Object> parameters;
    
    // Getters and setters
    public String getPatientId() { return patientId; }
    public void setPatientId(String patientId) { this.patientId = patientId; }
    public String getPredictionType() { return predictionType; }
    public void setPredictionType(String predictionType) { this.predictionType = predictionType; }
    public double getThreshold() { return threshold; }
    public void setThreshold(double threshold) { this.threshold = threshold; }
    public String getTimeHorizon() { return timeHorizon; }
    public void setTimeHorizon(String timeHorizon) { this.timeHorizon = timeHorizon; }
    public Map<String, Object> getParameters() { return parameters; }
    public void setParameters(Map<String, Object> parameters) { this.parameters = parameters; }
}

/**
 * 予測アラート
 */
class PredictiveAlert {
    private String alertId;
    private String patientId;
    private String predictionType;
    private double threshold;
    private String timeHorizon;
    private String status;
    private LocalDateTime createdAt;
    
    // Getters and setters
    public String getAlertId() { return alertId; }
    public void setAlertId(String alertId) { this.alertId = alertId; }
    public String getPatientId() { return patientId; }
    public void setPatientId(String patientId) { this.patientId = patientId; }
    public String getPredictionType() { return predictionType; }
    public void setPredictionType(String predictionType) { this.predictionType = predictionType; }
    public double getThreshold() { return threshold; }
    public void setThreshold(double threshold) { this.threshold = threshold; }
    public String getTimeHorizon() { return timeHorizon; }
    public void setTimeHorizon(String timeHorizon) { this.timeHorizon = timeHorizon; }
    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }
    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
}

/**
 * バイタルサインデータ
 */
class VitalSignsData {
    private Map<String, Double> vitalSigns;
    private boolean anomalyDetected;
    private String riskLevel;
    private LocalDateTime timestamp;
    
    // Getters and setters
    public Map<String, Double> getVitalSigns() { return vitalSigns; }
    public void setVitalSigns(Map<String, Double> vitalSigns) { this.vitalSigns = vitalSigns; }
    public boolean isAnomalyDetected() { return anomalyDetected; }
    public void setAnomalyDetected(boolean anomalyDetected) { this.anomalyDetected = anomalyDetected; }
    public String getRiskLevel() { return riskLevel; }
    public void setRiskLevel(String riskLevel) { this.riskLevel = riskLevel; }
    public LocalDateTime getTimestamp() { return timestamp; }
    public void setTimestamp(LocalDateTime timestamp) { this.timestamp = timestamp; }
}

/**
 * 異常検知
 */
class AnomalyDetection {
    private String anomalyId;
    private String patientId;
    private String anomalyType;
    private String severity;
    private LocalDateTime timestamp;
    private Map<String, Object> details;
    
    // Getters and setters
    public String getAnomalyId() { return anomalyId; }
    public void setAnomalyId(String anomalyId) { this.anomalyId = anomalyId; }
    public String getPatientId() { return patientId; }
    public void setPatientId(String patientId) { this.patientId = patientId; }
    public String getAnomalyType() { return anomalyType; }
    public void setAnomalyType(String anomalyType) { this.anomalyType = anomalyType; }
    public String getSeverity() { return severity; }
    public void setSeverity(String severity) { this.severity = severity; }
    public LocalDateTime getTimestamp() { return timestamp; }
    public void setTimestamp(LocalDateTime timestamp) { this.timestamp = timestamp; }
    public Map<String, Object> getDetails() { return details; }
    public void setDetails(Map<String, Object> details) { this.details = details; }
}
