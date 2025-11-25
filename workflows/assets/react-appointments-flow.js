import React, { useCallback, useEffect, useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import {
  ReactFlow,
  Controls,
  Handle,
  addEdge,
  useNodesState,
  useEdgesState,
} from "@xyflow/react";

const h = React.createElement;

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

const steps = [
  { id: "a", title: "Incoming Message", sub: "WhatsApp / Webhook" },
  { id: "b", title: "Capture Availability", sub: "Form / Bot" },
  { id: "c", title: "Book Appointment", sub: "Google Calendar" },
  { id: "d", title: "Send Confirmation", sub: "Gmail" },
];

function buildGraph(layout) {
  const horizontal = layout !== "mobile";
  const baseY = 110;
  const gapX = 210;
  const gapY = 120;
  const xFor = (i) => (horizontal ? 30 + i * gapX : 140);
  const yFor = (i) => (horizontal ? baseY : 60 + i * gapY);
  const nodes = steps.map((s, i) => ({ id: s.id, type: "step", position: { x: xFor(i), y: yFor(i) }, data: { title: s.title, sub: s.sub } }));
  const edges = steps.slice(1).map((s, i) => ({
    id: `e-${steps[i].id}-${s.id}`,
    source: steps[i].id,
    target: s.id,
    sourceHandle: horizontal ? "right" : "bottom",
    targetHandle: horizontal ? "left" : "top",
  }));
  return { nodes, edges };
}

function AppointmentsFlow() {
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
          { ...params, animated: true, style: { stroke: "var(--edge)", strokeWidth: 3 } },
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
      className: "bg-transparent",
    },
    h(Controls, { position: "top-left" }),
  );
}

function mount() {
  const el = document.getElementById("rf-canvas-appointments");
  if (el) createRoot(el).render(h(AppointmentsFlow));
}
if (document.readyState === "loading") {
  window.addEventListener("DOMContentLoaded", mount);
} else {
  mount();
}

