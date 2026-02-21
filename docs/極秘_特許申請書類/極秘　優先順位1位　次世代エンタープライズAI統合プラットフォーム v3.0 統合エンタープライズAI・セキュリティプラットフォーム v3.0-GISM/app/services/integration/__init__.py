"""
Integration Services
統合サービス（v2.0 + v8.0統合機能）
"""

from .quantum_optimized_fusion import QuantumOptimizedFusion, QuantumOptimizedFusionResult

# IntegrationServiceはapp/services/integration.pyにあるため、後方互換性のために再エクスポート
import sys
import os
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
integration_py = os.path.join(parent_dir, 'integration.py')
if os.path.exists(integration_py):
    import importlib.util
    spec = importlib.util.spec_from_file_location("integration", integration_py)
    integration_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(integration_module)
    IntegrationService = integration_module.IntegrationService
    __all__ = [
        'QuantumOptimizedFusion',
        'QuantumOptimizedFusionResult',
        'IntegrationService'
    ]
else:
    __all__ = [
        'QuantumOptimizedFusion',
        'QuantumOptimizedFusionResult'
    ]

