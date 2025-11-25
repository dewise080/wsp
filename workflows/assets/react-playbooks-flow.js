import React, { useCallback, useEffect, useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import {
  ReactFlow,
  Background,
  Controls,
  Handle,
  addEdge,
  useNodesState,
  useEdgesState,
} from "@xyflow/react";

const h = React.createElement;

// Simple CRM-focused step node
function StepNode({ data }) {
  return h(
    "div",
    { className: "step" },
    h(Handle, { type: "target", position: "left", id: "left" }),
    h(Handle, { type: "source", position: "right", id: "right" }),
    h(Handle, { type: "target", position: "top", id: "top" }),
    h(Handle, { type: "source", position: "bottom", id: "bottom" }),
    h(
      "div",
      null,
      h("div", { className: "title" }, data.title),
      data.sub ? h("div", { className: "sub" }, data.sub) : null,
    ),
  );
}

const nodeTypes = { step: StepNode };

function computeLayout() {
  return window.innerWidth < 768 ? "mobile" : "desktop";
}

// Build a simple linear flow focusing on CRM integration
const steps = [
  { id: "a", title: "Incoming Message", sub: "WhatsApp / Webhook" },
  { id: "b", title: "Qualify Lead", sub: "Ask key questions" },
  { id: "c", title: "Sync to CRM", sub: "Create/Update contact" },
  { id: "d", title: "Create Deal", sub: "Stage + owner" },
  { id: "e", title: "Notify Team", sub: "Slack / Email" },
];

function buildGraph(layout) {
  const horizontal = layout !== "mobile";
  const baseY = 110;
  const gapX = 210;
  const gapY = 120;
  const xFor = (i) => (horizontal ? 30 + i * gapX : 140);
  const yFor = (i) => (horizontal ? baseY : 60 + i * gapY);
  const nodes = steps.map((s, i) => ({
    id: s.id,
    type: "step",
    position: { x: xFor(i), y: yFor(i) },
    data: { title: s.title, sub: s.sub },
  }));
  const edges = steps.slice(1).map((s, i) => ({
    id: `e-${steps[i].id}-${s.id}`,
    source: steps[i].id,
    target: s.id,
    sourceHandle: horizontal ? "right" : "bottom",
    targetHandle: horizontal ? "left" : "top",
  }));
  return { nodes, edges };
}

function PlaybooksFlow() {
  const [layout, setLayout] = useState(computeLayout());
  const initial = useMemo(() => buildGraph(layout), [layout]);
  const [nodes, setNodes, onNodesChange] = useNodesState(initial.nodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initial.edges);

  useEffect(() => {
    const update = () => setLayout(computeLayout());
    window.addEventListener("resize", update);
    return () => window.removeEventListener("resize", update);
  }, []);

  useEffect(() => {
    const g = buildGraph(layout);
    setNodes(g.nodes);
    setEdges(g.edges);
  }, [layout, setNodes, setEdges]);
  const onConnect = useCallback(
    (params) =>
      setEdges((eds) =>
        addEdge(
          {
            ...params,
            animated: true,
            style: { stroke: "var(--edge)", strokeWidth: 3 },
          },
          eds,
        ),
      ),
    [],
  );

  return h(
    ReactFlow,
    {
      nodes,
      edges,
      onNodesChange,
      onEdgesChange,
      onConnect,
      fitView: true,
      nodesDraggable: true,
      proOptions: { hideAttribution: true },
      nodeTypes,
      defaultEdgeOptions: {
        animated: true,
        style: { stroke: "var(--edge)", strokeWidth: 3 },
      },
      className: "bg-transparent",
    },
    // Transparent background (no dots)
    h(Controls, { position: "top-left" }),
  );
}

function mountPlaybooks() {
  const mountEl = document.getElementById("rf-canvas-playbooks");
  if (mountEl) {
    createRoot(mountEl).render(h(PlaybooksFlow));
  }
}

if (document.readyState === "loading") {
  window.addEventListener("DOMContentLoaded", mountPlaybooks);
} else {
  mountPlaybooks();
}
