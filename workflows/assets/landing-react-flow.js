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

// JSON loader (preferred)
async function loadJsonFlow() {
  const res = await fetch("assets/flow-data.json", { cache: "no-store" });
  if (!res.ok) throw new Error("no-json");
  return await res.json();
}

function Handles({ data, color }) {
  const layout = data?.layout || "desktop"; // desktop or mobile
  const cfg = data?.handleConfig || "middle"; // first | middle | last
  // Keep size via utilities; color is handled by node variant CSS if present
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
          data.iconSrc
            ? h("img", {
                src: data.iconSrc,
                alt: data.iconAlt || "",
                className: "w-5 h-5 opacity-90",
                loading: "lazy",
              })
            : h("span", { className: "text-sm opacity-90" }, data.icon || "•"),
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
          Array.isArray(data.items) && data.items.length
            ? h(
                "ul",
                { className: "mt-2 flex flex-col gap-1" },
                ...data.items.map((it) =>
                  h(
                    "li",
                    { className: "flex items-center gap-2" },
                    h(
                      "span",
                      {
                        className:
                          "w-4 h-4 rounded-full bg-white flex items-center justify-center",
                      },
                      h("img", {
                        src: `https://cdn.simpleicons.org/${it.slug}${it.color ? "/" + it.color : ""}`,
                        alt: it.name,
                        className: "w-3 h-3",
                        loading: "lazy",
                      }),
                    ),
                    h(
                      "span",
                      { className: "text-xs text-white" },
                      it.name,
                    ),
                  ),
                ),
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

function arrangeLinear(nodes, edges, layout) {
  const byId = new Map(nodes.map((n) => [n.id, n]));
  const incoming = new Map();
  const outgoing = new Map();
  for (const n of nodes) {
    incoming.set(n.id, 0);
    outgoing.set(n.id, []);
  }
  for (const e of edges) {
    if (byId.has(e.source) && byId.has(e.target)) {
      incoming.set(e.target, (incoming.get(e.target) || 0) + 1);
      outgoing.get(e.source).push(e.target);
    }
  }
  // Pick start: prefer eventNode, else any with no incoming, else first
  let start = nodes.find((n) => n.type === "eventNode")?.id;
  if (!start) {
    const noIn = nodes.find((n) => (incoming.get(n.id) || 0) === 0);
    start = noIn ? noIn.id : nodes[0]?.id;
  }
  const visited = new Set();
  const order = [];
  const q = [];
  if (start) q.push(start);
  while (q.length) {
    const id = q.shift();
    if (!id || visited.has(id)) continue;
    visited.add(id);
    order.push(id);
    for (const t of outgoing.get(id) || []) {
      if (!visited.has(t)) q.push(t);
    }
  }
  for (const n of nodes) if (!visited.has(n.id)) order.push(n.id);

  const horizontal = layout !== "mobile";
  const startX = 100;
  const startY = 140;
  const gapX = 220;
  const gapY = 160;
  const positioned = new Map();
  order.forEach((id, idx) => {
    const x = horizontal ? startX + gapX * idx : 140;
    const y = horizontal ? 200 : startY + gapY * idx;
    positioned.set(id, { x, y });
  });
  return nodes.map((n) => ({ ...n, position: positioned.get(n.id) || n.position }));
}

function defaultGraph(layout) {
  const nodes = [
    {
      id: "1",
      type: "eventNode",
      position: { x: 100, y: 120 },
      data: {
        label: "WhatsApp Incoming Message",
        description: "Starts when a message arrives",
        iconSrc: "https://cdn.simpleicons.org/whatsapp/25D366",
        iconAlt: "WhatsApp",
        layout,
      },
    },
    {
      id: "2",
      type: "agentNode",
      position: { x: 320, y: 200 },
      data: {
        label: "AI Agent",
        iconSrc: "https://cdn.simpleicons.org/openai/ffffff",
        iconAlt: "OpenAI",
        layout,
      },
    },
    {
      id: "3",
      type: "connectorNode",
      position: { x: 760, y: 360 },
      data: {
        label: "Integrations",
        description: "Popular services",
        items: [
          { slug: "googlecalendar", name: "Google Calendar", color: "1A73E8" },
          { slug: "googlesheets", name: "Google Sheets", color: "0F9D58" },
          { slug: "slack", name: "Slack", color: "4A154B" },
          { slug: "stripe", name: "Stripe", color: "635BFF" },
          { slug: "github", name: "GitHub", color: "ffffff" },
          { slug: "gmail", name: "Gmail", color: "EA4335" },
        ],
        layout,
      },
    },
    {
      id: "4",
      type: "logicNode",
      position: { x: 540, y: 140 },
      data: { label: "Business Logic", layout },
    },
    {
      id: "5",
      type: "actionNode",
      position: { x: 800, y: 220 },
      data: { label: "Execute Action", layout },
    },
    {
      id: "6",
      type: "agentNode",
      position: { x: 540, y: 280 },
      data: {
        label: "Multi-Agent",
        description: "Orchestrated AI",
        iconSrc: "https://cdn.simpleicons.org/openai/ffffff",
        iconAlt: "OpenAI",
        layout,
      },
    },
    {
      id: "7",
      type: "eventNode",
      position: { x: 1000, y: 220 },
      data: {
        label: "Reply to message",
        iconSrc: "https://cdn.simpleicons.org/whatsapp/25D366",
        iconAlt: "WhatsApp",
        layout,
      },
    },
  ];
  const edges = [
    { id: "e1-2", source: "1", target: "2" },
    { id: "e2-6", source: "2", target: "6" },
    { id: "e2-4", source: "2", target: "4" },
    { id: "e6-3", source: "6", target: "3" },
    { id: "e4-5", source: "4", target: "5" },
    { id: "e6-5", source: "6", target: "5" },
    { id: "e5-7", source: "5", target: "7" },
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

  const nodesWithLayout = nodes.map((n) => ({ ...n, data: { ...n.data, layout } }));
  const arranged = arrangeLinear(nodesWithLayout, handledEdges, layout);
  const withCfg = withHandleConfig(arranged, handledEdges);
  return { nodes: withCfg, edges: handledEdges };
}

function buildGraphFromJSON(layout, json) {
  const nodes = (json.nodes || []).map((n) => {
    const pos = layout === "mobile" ? n.posMobile || n.posDesktop : n.posDesktop || n.posMobile;
    const data = {
      label: n.label || "",
      description: n.description || undefined,
      layout,
    };
    if (n.iconSlug) {
      data.iconSrc = `https://cdn.simpleicons.org/${n.iconSlug}${n.iconColor ? "/" + n.iconColor : ""}`;
      data.iconAlt = n.iconAlt || n.label || n.iconSlug;
    }
    if (Array.isArray(n.items)) data.items = n.items;
    return { id: String(n.id), type: n.type || "connectorNode", position: pos || { x: 140, y: 140 }, data };
  });

  const edges = (json.edges || []).map((e, idx) => ({ id: String(e.id || `e${idx}`), source: String(e.source), target: String(e.target) }));

  const styled = edges.map((e) => ({
    ...e,
    style: { stroke: "#3b82f6", strokeWidth: 3 },
    animated: true,
  }));

  const handled = styled.map((e) =>
    layout === "mobile"
      ? { ...e, sourceHandle: "bottom", targetHandle: "top" }
      : { ...e, sourceHandle: "right", targetHandle: "left" },
  );

  const nodesWithLayout = nodes.map((n) => ({ ...n, data: { ...n.data, layout } }));
  const withCfg = withHandleConfig(nodesWithLayout, handled);
  return { nodes: withCfg, edges: handled };
}

function LandingFlow() {
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
    let cancelled = false;
    (async () => {
      try {
        const json = await loadJsonFlow();
        if (cancelled) return;
        const next = buildGraphFromJSON(layout, json);
        setNodes(next.nodes);
        setEdges(next.edges);
      } catch (err) {
        const next = defaultGraph(layout);
        setNodes(next.nodes);
        setEdges(next.edges);
      }
    })();
    return () => {
      cancelled = true;
    };
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

function mountLanding() {
  const el = document.getElementById("rf-canvas-landing");
  if (el) createRoot(el).render(h(LandingFlow));
}

if (document.readyState === "loading") {
  window.addEventListener("DOMContentLoaded", mountLanding);
} else {
  mountLanding();
}
