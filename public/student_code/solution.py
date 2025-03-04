import sys
import os

# Agregar manualmente la ruta del directorio raíz del proyecto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import networkx as nx
import random
from typing import Dict, List, Literal
from public.lib.interfaces import CityGraph, ProxyData, PolicyResult
from public.student_code.convert_to_df import convert_edge_data_to_df, convert_node_data_to_df

class EvacuationPolicy:
    def __init__(self):
        self.policy_type = "policy_2"

    def set_policy(self, policy_type: Literal["policy_1", "policy_2", "policy_3", "policy_4"]):
        self.policy_type = policy_type

    def plan_evacuation(self, city: CityGraph, proxy_data: ProxyData, max_resources: int) -> PolicyResult:
        if self.policy_type == "policy_1":
            return self._policy_1(city, max_resources)
        elif self.policy_type == "policy_2":
            return self._policy_2(city, proxy_data, max_resources)
        elif self.policy_type == "policy_3":
            return self._policy_3(city, proxy_data, max_resources)
        else:
            return self._policy_4(city, proxy_data, max_resources)

    def _policy_1(self, city: CityGraph, max_resources: int) -> PolicyResult:
        """
        Política 1: A* con distribución aleatoria de recursos
        - No se cuenta con información externa.
        - Se usa A* para buscar la ruta más corta.
        - Si no hay camino, se asignan 0 recursos.
        """
        def heuristic(node1, node2):
            x1, y1 = city.graph.nodes[node1]['pos']
            x2, y2 = city.graph.nodes[node2]['pos']
            return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5  # Distancia euclidiana

        target = min(city.extraction_nodes, key=lambda node: heuristic(city.starting_node, node))

        try:
            path = nx.astar_path(city.graph, city.starting_node, target, heuristic=heuristic, weight='weight')
            resources = {
                'explosives': random.randint(0, max_resources // 3),
                'ammo': random.randint(0, max_resources // 3),
                'radiation_suits': random.randint(0, max_resources // 3)
            }
        except nx.NetworkXNoPath:
            path = [city.starting_node]
            resources = {'explosives': 0, 'ammo': 0, 'radiation_suits': 0}

        return PolicyResult(path, resources)

    def _policy_2(self, city: CityGraph, proxy_data: ProxyData, max_resources: int) -> PolicyResult:
        """
        Política 2: Uso de proxys de actividad sísmica, radiación, población, emergencias y temperatura.
        - Se evalúan los riesgos basados en sensores.
        - Se buscan rutas alternativas si los valores de riesgo superan los umbrales.
        """
        def weight_function(u, v, edge_attrs):
            base_weight = edge_attrs.get('weight', 1)

            # Obtener valores de los proxys
            proxy = proxy_data.edge_data.get((u, v), {})
            seismic = proxy.get('seismic_activity', 0)
            radiation = proxy.get('radiation', 0)
            population_density = proxy.get('population_density', 0)
            emergency_calls = proxy.get('emergency_calls', 0)
            thermal_activity = proxy.get('thermal_activity', 0)
            structure_integrity = proxy.get('structure_integrity', 1)

            # Ajustar el peso de la ruta en función de los proxys
            if seismic > 0.75 and max_resources < 2:
                return float('inf')  # Evitar si hay pocos explosivos
            if radiation == 1 or (0.4 <= radiation <= 0.75 and max_resources < 1):
                return float('inf')  # Evitar si hay radiación alta y pocos trajes
            if population_density == 1 and max_resources < 5:
                return float('inf')  # Evitar si hay mucha población y pocas balas
            if emergency_calls > 0.8:
                return float('inf')  # Evitar si hay muchas llamadas de emergencia
            if thermal_activity and max_resources < 3:
                return float('inf')  # Evitar si hay actividad térmica y pocas balas
            if structure_integrity < 0.3:
                return float('inf')  # Evitar si la estructura es frágil

            return base_weight  # Si no hay restricciones, usar el peso base

        # Seleccionar el mejor punto de extracción accesible
        target = min(city.extraction_nodes, key=lambda node: nx.shortest_path_length(city.graph, city.starting_node, node, weight='weight'))

        try:
            path = nx.shortest_path(city.graph, city.starting_node, target, weight=lambda u, v, d: weight_function(u, v, d))
        except nx.NetworkXNoPath:
            path = [city.starting_node]

        resources = {
            'explosives': random.randint(0, max_resources // 3),
            'ammo': random.randint(0, max_resources // 3),
            'radiation_suits': random.randint(0, max_resources // 3)
        }

        return PolicyResult(path, resources)

    def _policy_3(self, city: CityGraph, proxy_data: ProxyData, max_resources: int) -> PolicyResult:
        """
        Política 3: Uso de datos históricos para tomar decisiones
        - Se analiza el success rate de misiones previas.
        - Se ajusta la estrategia con base en tendencias observadas.
        """
        past_data = getattr(proxy_data, "historical_data", {})

        if not past_data:
            print("⚠️ No se encontraron datos históricos, usando solo el grafo base.")
            return self._policy_1(city, max_resources)

        edge_success_rates = {
            edge: past_data.get(edge, {}).get('success_rate', 1) for edge in city.graph.edges
        }

        def weight_function(u, v, edge_attrs):
            base_weight = edge_attrs.get('weight', 1)
            success_factor = edge_success_rates.get((u, v), 1)
            return base_weight * (2 - success_factor)

        target = min(city.extraction_nodes, key=lambda node: nx.shortest_path_length(city.graph, city.starting_node, node, weight='weight'))

        try:
            path = nx.shortest_path(city.graph, city.starting_node, target, weight=lambda u, v, d: weight_function(u, v, d))
        except nx.NetworkXNoPath:
            path = [city.starting_node]

        resources = {
            'explosives': max_resources // 5,
            'ammo': max_resources // 2,
            'radiation_suits': max_resources // 3
        }

        return PolicyResult(path, resources)

    def _policy_4(self, city: CityGraph, proxy_data: ProxyData, max_resources: int) -> PolicyResult:
        """
        Política 4: Simulación extrema sin moral.
        - Se envían equipos sin recursos para recopilar datos.
        - Se maximizan las pruebas para entender el entorno.
        """
        target = random.choice(city.extraction_nodes)

        try:
            path = nx.shortest_path(city.graph, city.starting_node, target, weight='weight')
        except nx.NetworkXNoPath:
            path = [city.starting_node]

        resources = {'explosives': 0, 'ammo': 0, 'radiation_suits': 0}

        return PolicyResult(path, resources)

    
    
