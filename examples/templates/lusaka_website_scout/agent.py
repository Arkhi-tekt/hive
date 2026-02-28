"""Agent graph construction for Lusaka Website Scout Agent."""

from framework.graph import EdgeSpec, EdgeCondition, Goal, SuccessCriterion, Constraint
from framework.graph.edge import GraphSpec
from framework.graph.executor import ExecutionResult, GraphExecutor
from framework.runtime.event_bus import EventBus
from framework.runtime.core import Runtime
from framework.llm import LiteLLMProvider
from framework.runner.tool_registry import ToolRegistry

from .config import default_config, metadata
from .nodes import (
    discovery_node,
    audit_node,
    report_node,
)

# Goal definition
goal = Goal(
    id="lusaka-website-scout",
    name="Lusaka Website Scout",
    description=(
        "Find local businesses in Lusaka, Zambia within a specific category, "
        "audit their websites for design flaws, and report high-priority leads."
    ),
    success_criteria=[
        SuccessCriterion(
            id="business-discovery",
            description="Successfully identifies at least 5 local businesses with website URLs",
            metric="discovery_count",
            target=">= 5 businesses",
            weight=0.3,
        ),
        SuccessCriterion(
            id="quality-audit",
            description="Provides a qualitative audit for each website found, identifying design and technical flaws",
            metric="audit_depth",
            target="Audit for every found site",
            weight=0.4,
        ),
        SuccessCriterion(
            id="actionable-reporting",
            description="Deliver a report with clear 'Sales Pitch Tips' for the worst sites",
            metric="report_quality",
            target=" Actionable insights provided",
            weight=0.3,
        ),
    ],
    constraints=[
        Constraint(
            id="local-focus",
            description="Must focus strictly on businesses located in Lusaka, Zambia",
            constraint_type="safety",
            category="location",
        ),
    ],
)

# Node list
nodes = [
    discovery_node,
    audit_node,
    report_node,
]

# Edge definitions
edges = [
    EdgeSpec(
        id="discovery-to-audit",
        source="discovery",
        target="audit",
        condition=EdgeCondition.ON_SUCCESS,
        priority=1,
    ),
    EdgeSpec(
        id="audit-to-report",
        source="audit",
        target="report",
        condition=EdgeCondition.ON_SUCCESS,
        priority=1,
    ),
]

# Graph configuration
entry_node = "discovery"
entry_points = {"start": "discovery"}
pause_nodes = []
terminal_nodes = ["report"]

class LusakaWebsiteScoutAgent:
    def __init__(self, config=None):
        self.config = config or default_config
        self.goal = goal
        self.nodes = nodes
        self.edges = edges
        self.entry_node = entry_node
        self.entry_points = entry_points
        self.pause_nodes = pause_nodes
        self.terminal_nodes = terminal_nodes
        self._executor: GraphExecutor | None = None
        self._graph: GraphSpec | None = None

    def _build_graph(self) -> GraphSpec:
        return GraphSpec(
            id="lusaka-website-scout-graph",
            goal_id=self.goal.id,
            version="0.1.0",
            entry_node=self.entry_node,
            entry_points=self.entry_points,
            terminal_nodes=self.terminal_nodes,
            pause_nodes=self.pause_nodes,
            nodes=self.nodes,
            edges=self.edges,
            default_model=self.config.model,
            max_tokens=self.config.max_tokens,
            loop_config={
                "max_iterations": 30,
                "max_tool_calls_per_turn": 10,
                "max_history_tokens": 64000,
            },
        )

    def _setup(self) -> GraphExecutor:
        from pathlib import Path
        storage_path = Path.home() / ".hive" / "lusaka_website_scout"
        storage_path.mkdir(parents=True, exist_ok=True)

        event_bus = EventBus()
        tool_registry = ToolRegistry()

        mcp_config_path = Path(__file__).parent / "mcp_servers.json"
        if mcp_config_path.exists():
            tool_registry.load_mcp_config(mcp_config_path)

        llm = LiteLLMProvider(
            model=self.config.model,
            api_key=self.config.api_key,
            api_base=self.config.api_base,
        )

        tool_executor = tool_registry.get_executor()
        tools = list(tool_registry.get_tools().values())

        self._graph = self._build_graph()
        runtime = Runtime(storage_path)

        self._executor = GraphExecutor(
            runtime=runtime,
            llm=llm,
            tools=tools,
            tool_executor=tool_executor,
            event_bus=event_bus,
            storage_path=storage_path,
            loop_config=self._graph.loop_config,
        )
        return self._executor

    async def run(self, context: dict) -> ExecutionResult:
        if self._executor is None:
            self._setup()

        return await self._executor.execute(
            graph=self._graph,
            goal=self.goal,
            input_data=context,
        )

# Default instance
default_agent = LusakaWebsiteScoutAgent()
