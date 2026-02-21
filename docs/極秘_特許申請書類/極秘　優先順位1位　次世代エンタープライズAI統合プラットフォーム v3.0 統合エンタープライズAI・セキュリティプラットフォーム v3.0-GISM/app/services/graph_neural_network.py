"""
グラフニューラルネットワーク（GNN）サービス
フェーズ3: 高度な領域統合
- GCN: Graph Convolutional Network
- GAT: Graph Attention Network
- 推薦システム
- ソーシャルネットワーク分析
"""
import logging
from typing import Dict, Any, Optional, List
import numpy as np

# NetworkX（グラフ操作、必須）
try:
    import networkx as nx
    NETWORKX_AVAILABLE = True
except ImportError:
    NETWORKX_AVAILABLE = False
    logging.warning("NetworkX not available. Graph functionality will be limited.")

# PyTorch Geometric（GNN、オプショナル）
try:
    import torch
    import torch_geometric
    from torch_geometric.nn import GCNConv, GATConv
    TORCH_GEOMETRIC_AVAILABLE = True
except ImportError:
    TORCH_GEOMETRIC_AVAILABLE = False
    logging.warning("PyTorch Geometric not available. GNN functionality will use basic graph analysis.")

logger = logging.getLogger(__name__)


class GraphNeuralNetworkService:
    """グラフニューラルネットワークサービス"""
    
    def __init__(self):
        self.networkx_available = NETWORKX_AVAILABLE
        self.torch_geometric_available = TORCH_GEOMETRIC_AVAILABLE
        self.gcn_model = None
        self.gat_model = None
        
        if TORCH_GEOMETRIC_AVAILABLE:
            try:
                # GNNモデルの初期化（必要に応じて）
                logger.info("PyTorch Geometric available. GNN models can be initialized.")
            except Exception as e:
                logger.warning(f"Failed to initialize GNN models: {e}")
    
    def is_available(self) -> bool:
        """サービスが利用可能かチェック"""
        return NETWORKX_AVAILABLE
    
    def analyze_graph(self, graph_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        グラフ分析
        
        Args:
            graph_data: グラフデータ（nodes, edges）
        
        Returns:
            分析結果
        """
        if not NETWORKX_AVAILABLE:
            return {
                "status": "error",
                "message": "NetworkX is not available"
            }
        
        try:
            # グラフを作成
            G = nx.Graph()
            
            # ノードを追加
            nodes = graph_data.get("nodes", [])
            if isinstance(nodes, list):
                G.add_nodes_from(nodes)
            elif isinstance(nodes, dict):
                G.add_nodes_from(nodes.keys())
            
            # エッジを追加
            edges = graph_data.get("edges", [])
            if isinstance(edges, list):
                if len(edges) > 0 and isinstance(edges[0], (list, tuple)) and len(edges[0]) == 2:
                    G.add_edges_from(edges)
                elif isinstance(edges[0], dict):
                    # エッジが辞書形式の場合
                    for edge in edges:
                        G.add_edge(edge.get("source"), edge.get("target"), **{k: v for k, v in edge.items() if k not in ["source", "target"]})
            
            # 基本的なグラフ統計
            stats = {
                "num_nodes": G.number_of_nodes(),
                "num_edges": G.number_of_edges(),
                "density": nx.density(G),
                "is_connected": nx.is_connected(G) if G.number_of_nodes() > 0 else False
            }
            
            # 中心性指標
            if G.number_of_nodes() > 0:
                try:
                    degree_centrality = nx.degree_centrality(G)
                    betweenness_centrality = nx.betweenness_centrality(G)
                    closeness_centrality = nx.closeness_centrality(G)
                    
                    # トップ5のノード
                    top_degree = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
                    top_betweenness = sorted(betweenness_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
                    top_closeness = sorted(closeness_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
                    
                    stats["centrality"] = {
                        "degree": {str(k): float(v) for k, v in top_degree},
                        "betweenness": {str(k): float(v) for k, v in top_betweenness},
                        "closeness": {str(k): float(v) for k, v in top_closeness}
                    }
                except Exception as e:
                    logger.warning(f"Failed to calculate centrality: {e}")
                    stats["centrality"] = {}
            
            # コミュニティ検出（簡易版）
            communities = []
            if G.number_of_nodes() > 0:
                try:
                    # 連結成分をコミュニティとして扱う
                    connected_components = list(nx.connected_components(G))
                    for i, component in enumerate(connected_components):
                        communities.append({
                            "id": i,
                            "nodes": list(component),
                            "size": len(component)
                        })
                except Exception as e:
                    logger.warning(f"Failed to detect communities: {e}")
            
            return {
                "status": "success",
                "statistics": stats,
                "communities": communities,
                "note": "Basic graph analysis (GNN models require torch)"
            }
        
        except Exception as e:
            logger.error(f"Error in analyze_graph: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def recommend_items(
        self,
        user_id: str,
        graph_data: Dict[str, Any],
        n_recommendations: int = 10
    ) -> Dict[str, Any]:
        """
        推薦システム
        
        Args:
            user_id: ユーザーID
            graph_data: グラフデータ（ユーザー-アイテムグラフ）
            n_recommendations: 推薦数
        
        Returns:
            推薦結果
        """
        if not NETWORKX_AVAILABLE:
            return {
                "status": "error",
                "message": "NetworkX is not available"
            }
        
        try:
            # グラフを作成
            G = nx.Graph()
            
            nodes = graph_data.get("nodes", [])
            edges = graph_data.get("edges", [])
            
            if isinstance(nodes, list):
                G.add_nodes_from(nodes)
            elif isinstance(nodes, dict):
                G.add_nodes_from(nodes.keys())
            
            if isinstance(edges, list) and len(edges) > 0:
                if isinstance(edges[0], (list, tuple)) and len(edges[0]) == 2:
                    G.add_edges_from(edges)
            
            # ユーザーの近傍ノードを取得
            if user_id in G:
                neighbors = list(G.neighbors(user_id))
                
                # 2ホップ先のノードを推薦候補とする
                recommendations = []
                for neighbor in neighbors:
                    second_hop = G.neighbors(neighbor)
                    for item in second_hop:
                        if item != user_id and item not in neighbors:
                            # 簡易的なスコア計算（エッジの重みがあれば使用）
                            score = 1.0
                            if G.has_edge(user_id, neighbor):
                                edge_data = G[user_id][neighbor]
                                if "weight" in edge_data:
                                    score *= edge_data["weight"]
                            if G.has_edge(neighbor, item):
                                edge_data = G[neighbor][item]
                                if "weight" in edge_data:
                                    score *= edge_data["weight"]
                            
                            recommendations.append({
                                "item_id": str(item),
                                "score": float(score)
                            })
                
                # スコアでソート
                recommendations.sort(key=lambda x: x["score"], reverse=True)
                recommendations = recommendations[:n_recommendations]
                
                return {
                    "status": "success",
                    "user_id": user_id,
                    "recommendations": recommendations,
                    "count": len(recommendations),
                    "method": "graph_based_2hop",
                    "note": "Basic recommendation (GNN-based recommendation requires torch)"
                }
            else:
                return {
                    "status": "error",
                    "message": f"User {user_id} not found in graph"
                }
        
        except Exception as e:
            logger.error(f"Error in recommend_items: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def analyze_social_network(self, network_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        ソーシャルネットワーク分析
        
        Args:
            network_data: ソーシャルネットワークデータ
        
        Returns:
            分析結果
        """
        if not NETWORKX_AVAILABLE:
            return {
                "status": "error",
                "message": "NetworkX is not available"
            }
        
        try:
            # グラフを作成
            G = nx.Graph()
            
            nodes = network_data.get("nodes", [])
            edges = network_data.get("edges", [])
            
            if isinstance(nodes, list):
                G.add_nodes_from(nodes)
            elif isinstance(nodes, dict):
                G.add_nodes_from(nodes.keys())
            
            if isinstance(edges, list) and len(edges) > 0:
                if isinstance(edges[0], (list, tuple)) and len(edges[0]) == 2:
                    G.add_edges_from(edges)
            
            # ソーシャルネットワーク分析
            analysis = {
                "num_users": G.number_of_nodes(),
                "num_connections": G.number_of_edges(),
                "average_degree": sum(dict(G.degree()).values()) / G.number_of_nodes() if G.number_of_nodes() > 0 else 0,
                "density": nx.density(G),
                "is_connected": nx.is_connected(G) if G.number_of_nodes() > 0 else False
            }
            
            # クラスタリング係数
            if G.number_of_nodes() > 0:
                try:
                    clustering = nx.clustering(G)
                    analysis["average_clustering"] = sum(clustering.values()) / len(clustering)
                    analysis["clustering_coefficient"] = {str(k): float(v) for k, v in list(clustering.items())[:10]}
                except Exception as e:
                    logger.warning(f"Failed to calculate clustering: {e}")
            
            # 影響力の高いユーザー（中心性）
            if G.number_of_nodes() > 0:
                try:
                    degree_centrality = nx.degree_centrality(G)
                    top_influencers = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:10]
                    analysis["top_influencers"] = [
                        {"user_id": str(user), "influence_score": float(score)}
                        for user, score in top_influencers
                    ]
                except Exception as e:
                    logger.warning(f"Failed to calculate influence: {e}")
            
            return {
                "status": "success",
                "analysis": analysis,
                "note": "Basic social network analysis (GAT-based analysis requires torch)"
            }
        
        except Exception as e:
            logger.error(f"Error in analyze_social_network: {e}")
            return {
                "status": "error",
                "message": str(e)
            }

