import React, { useEffect, useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import {
  ReactFlow,
  Background,
  Controls,
  Handle,
  useNodesState,
  useEdgesState,
  addEdge,
} from "@xyflow/react";

const h = React.createElement;

function Handles({ data, color }) {
  const layout = data?.layout || "desktop"; // desktop or mobile
  const cfg = data?.handleConfig || "middle"; // first | middle | last
  // Size via utility classes; color via parent variant styles in CSS
  const cls = "w-3 h-3";
  if (cfg === "first") {
    return layout === "desktop"
    ? h(Handle, {
      type: "source",
      position: "right",
      id: "right",
      className: cls,
    })
    : h(Handle, {
      type: "source",
      position: "bottom",
      id: "bottom",
      className: cls,
    });
  }
  if (cfg === "last") {
    return layout === "desktop"
    ? h(Handle, {
      type: "target",
      position: "left",
      id: "left",
      className: cls,
    })
    : h(Handle, {
      type: "target",
      position: "top",
      id: "top",
      className: cls,
    });
  }
  return h(
    React.Fragment,
    null,
    h(Handle, { type: "target", position: "top", id: "top", className: cls }),
    h(Handle, {
      type: "source",
      position: "bottom",
      id: "bottom",
      className: cls,
    }),
    h(Handle, { type: "target", position: "left", id: "left", className: cls }),
    h(Handle, {
      type: "source",
      position: "right",
      id: "right",
      className: cls,
    }),
  );
}

function cardBase(selected, colors) {
  const [from, to, border, hoverBorder, text] = colors;
  return (
    "relative px-6 py-4 shadow-2xl rounded-xl border-2 transition-all duration-300 " +
    `bg-gradient-to-br ${from} ${to} ` +
    `${border} backdrop-blur-sm ` +
    (selected
    ? hoverBorder.replace("hover:", "") + " shadow-md/50"
    : hoverBorder) +
    " hover:scale-105"
  );
}

function makeNode(color) {
  const map = {
    emerald: [
      "from-emerald-900/90",
      "to-emerald-800/90",
      "border-emerald-500/30",
      "hover:border-emerald-400/60",
      "text-emerald-100",
    ],
    purple: [
      "from-purple-900/90",
      "to-indigo-900/90",
      "border-purple-500/30",
      "hover:border-purple-400/60",
      "text-purple-100",
    ],
    blue: [
      "from-blue-900/90",
      "to-sky-900/90",
      "border-blue-500/30",
      "hover:border-blue-400/60",
      "text-blue-100",
    ],
    pink: [
      "from-pink-900/90",
      "to-rose-900/90",
      "border-pink-500/30",
      "hover:border-pink-400/60",
      "text-pink-100",
    ],
    orange: [
      "from-orange-900/90",
      "to-amber-900/90",
      "border-orange-500/30",
      "hover:border-orange-400/60",
      "text-orange-100",
    ],
  };
  return function Node({ data, selected }) {
    const colors = map[color] || map.blue;
    return h(
      "div",
      { className: `node ${color} ` + cardBase(selected, colors) },
      h(Handles, { data, color }),
      h(
        "div",
        { className: "flex items-center gap-3" },
        h(
          "div",
          {
            className:
              "w-8 h-8 rounded-lg bg-white/10 flex items-center justify-center",
          },
          h("span", { className: "text-sm opacity-90" }, data.icon || "•"),
        ),
        h(
          "div",
          null,
          h(
            "div",
            { className: `font-semibold ${colors[4]} text-sm` },
            data.label,
          ),
          data.description
            ? h(
                "div",
                { className: "text-xs text-white/70 mt-1" },
                data.description,
              )
            : null,
        ),
      ),
    );
  };
}

const nodeTypes = {
  eventNode: makeNode("emerald"),
  agentNode: makeNode("purple"),
  connectorNode: makeNode("blue"),
  actionNode: makeNode("pink"),
  logicNode: makeNode("orange"),
};

function computeLayout() {
  return window.innerWidth < 768 ? "mobile" : "desktop";
}

function withHandleConfig(nodes, edges) {
  return nodes.map((n) => {
    const hasIncoming = edges.some((e) => e.target === n.id);
    const hasOutgoing = edges.some((e) => e.source === n.id);
    let cfg = "middle";
    if (!hasIncoming && hasOutgoing) cfg = "first";
    else if (hasIncoming && !hasOutgoing) cfg = "last";
    return { ...n, data: { ...n.data, handleConfig: cfg } };
  });
}

function defaultGraph(layout) {
  const nodes = [
    {
      id: "1",
      type: "eventNode",
      position: { x: 100, y: 200 },
      data: { label: "Trigger", layout },
    },
    {
      id: "2",
      type: "agentNode",
      position: { x: 400, y: 200 },
      data: { label: "AI Agent", layout },
    },
    {
      id: "3",
      type: "connectorNode",
      position: { x: 360, y: 360 },
      data: { label: "Integrations", description: "1000+ Apps & APIs", layout },
    },
    {
      id: "4",
      type: "logicNode",
      position: { x: 700, y: 320 },
      data: { label: "Business Logic", layout },
    },
    {
      id: "5",
      type: "actionNode",
      position: { x: 1000, y: 200 },
      data: { label: "Execute Action", layout },
    },
    {
      id: "6",
      type: "agentNode",
      position: { x: 700, y: 80 },
      data: { label: "Multi-Agent", description: "Orchestrated AI", layout },
    },
  ];
  const edges = [
    { id: "e1-2", source: "1", target: "2" },
    { id: "e1-3", source: "1", target: "3" },
    { id: "e2-4", source: "2", target: "4" },
    { id: "e3-4", source: "3", target: "4" },
    { id: "e4-5", source: "4", target: "5" },
    { id: "e2-6", source: "2", target: "6" },
    { id: "e6-5", source: "6", target: "5" },
  ].map((e) => ({
    ...e,
    style: { stroke: "#3b82f6", strokeWidth: 3 },
    animated: true,
  }));

  // Adjust handle sides per layout
  const handledEdges = edges.map((e) =>
  layout === "mobile"
  ? { ...e, sourceHandle: "bottom", targetHandle: "top" }
  : { ...e, sourceHandle: "right", targetHandle: "left" },
  );

  const withCfg = withHandleConfig(
    nodes.map((n) => ({ ...n, data: { ...n.data, layout } })),
                                   handledEdges,
  );

  return { nodes: withCfg, edges: handledEdges };
}

function HeroFlow() {
  const [layout, setLayout] = useState("desktop");
  useEffect(() => {
    const update = () => setLayout(computeLayout());
    update();
    window.addEventListener("resize", update);
    return () => window.removeEventListener("resize", update);
  }, []);

  const initial = useMemo(() => defaultGraph(layout), [layout]);
  const [nodes, setNodes, onNodesChange] = useNodesState(initial.nodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initial.edges);

  useEffect(() => {
    // Rebuild graph when layout changes
    const next = defaultGraph(layout);
    setNodes(next.nodes);
    setEdges(next.edges);
  }, [layout, setNodes, setEdges]);

  const onConnect = React.useCallback(
    (params) =>
    setEdges((eds) =>
    addEdge(
      {
        ...params,
        animated: true,
        style: { stroke: "#3b82f6", strokeWidth: 3 },
      },
      eds,
    ),
    ),
    [setEdges],
  );

  return h(
    "div",
    {
      className:
      "w-full h-[550px] rounded-2xl overflow-hidden shadow-2xl border border-slate-700/50 bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900",
    },
    h(
      "div",
      {
        className:
        "p-4 border-b border-slate-700/50 bg-slate-900/80 backdrop-blur-sm",
      },
      h(
        "h3",
        { className: "text-lg font-semibold text-slate-100" },
        "Agent Workflow",
      ),
      h(
        "p",
        { className: "text-sm text-slate-400" },
        "Visual overview of triggers, agents, logic and actions",
      ),
    ),
    h(
      "div",
      { className: "h-[486px] relative" },
      h(
        ReactFlow,
        {
          nodes,
          edges,
          onNodesChange,
          onEdgesChange,
          onConnect,
          nodeTypes,
          proOptions: { hideAttribution: true },
          fitView: true,
          fitViewOptions: { padding: 0.2 },
          className: "bg-transparent",
        },
        h(Background, { variant: "dots" }),
        h(Controls, { position: "top-left" }),
      ),
    ),
  );
}

function mountHero() {
  const el = document.getElementById("rf-canvas-hero");
  if (el) createRoot(el).render(h(HeroFlow));
}

if (document.readyState === "loading") {
  window.addEventListener("DOMContentLoaded", mountHero);
} else {
  mountHero();
}
