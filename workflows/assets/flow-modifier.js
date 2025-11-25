import React, { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { createRoot } from "react-dom/client";
import {
  ReactFlow,
  Background,
  Controls,
  Handle,
  addEdge,
  useEdgesState,
  useNodesState,
} from "@xyflow/react";

const h = React.createElement;

// JSON helpers
async function loadJson() {
  const res = await fetch("../assets/sample-whatsapp.json", { cache: "no-store" });
  if (!res.ok) throw new Error("Missing sample-whatsapp.json");
  return await res.json();
}

function download(name, content, type = "text/plain") {
  const blob = new Blob([content], { type });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = name;
  a.click();
  URL.revokeObjectURL(a.href);
}

// no CSV anymore – JSON only

function Handles({ data }) {
  return h(React.Fragment, null,
    h(Handle, { type: "target", position: "top" }),
    h(Handle, { type: "source", position: "bottom" }),
    h(Handle, { type: "target", position: "left" }),
    h(Handle, { type: "source", position: "right" }),
  );
}

function NodeCard({ data }) {
  const typeToColor = { eventNode: "emerald", agentNode: "purple", connectorNode: "blue", actionNode: "pink", logicNode: "orange" };
  const color = typeToColor[data.type] || "blue";
  return h("div", { className: `node ${color} relative px-4 py-3 rounded-xl border-2` },
    h(Handles, { data }),
    h("div", { className: "flex items-center gap-2" },
      h("div", { className: "w-8 h-8 rounded-lg bg-white/10 flex items-center justify-center" },
        data.iconSlug ? h("img", { src: `https://cdn.simpleicons.org/${data.iconSlug}${data.iconColor?"/"+data.iconColor:""}`, className: "w-5 h-5", alt: data.iconAlt || data.iconSlug }) : h("span", { className: "text-sm" }, "•")
      ),
      h("div", null,
        h("div", { className: "text-sm font-semibold text-white" }, data.label || "Unnamed"),
        data.description ? h("div", { className: "text-xs text-white/70" }, data.description) : null,
        Array.isArray(data.items) && data.items.length ? h("ul", { className: "mt-1 flex flex-col gap-1" }, ...data.items.map((it) => h("li", { className: "flex items-center gap-2" }, h("span", { className: "w-4 h-4 bg-white rounded-full flex items-center justify-center" }, h("img", { src: `https://cdn.simpleicons.org/${it.slug}${it.color?"/"+it.color:""}`, className: "w-3 h-3", alt: it.name })), h("span", { className: "text-xs text-white" }, it.name)))) : null
      )
    )
  );
}

const nodeTypes = {
  eventNode: (p) => h(NodeCard, p),
  agentNode: (p) => h(NodeCard, p),
  connectorNode: (p) => h(NodeCard, p),
  actionNode: (p) => h(NodeCard, p),
  logicNode: (p) => h(NodeCard, p),
};

function Editor() {
  const [graph, setGraph] = useState({ nodes: [], edges: [] });
  const [mode, setMode] = useState("desktop");
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [selection, setSelection] = useState({ nodes: [], edges: [] });

  useEffect(() => {
    (async () => {
      try {
        const data = await loadJson();
        setGraph(data);
        const posKey = mode === "mobile" ? "posMobile" : "posDesktop";
        const gnodes = data.nodes.map((n) => ({
          id: n.id,
          type: n.type,
          position: n[posKey] || n.posDesktop || { x: 140, y: 140 },
          data: {
            type: n.type,
            label: n.label || "",
            description: n.description || "",
            iconSlug: n.iconSlug || "",
            iconColor: n.iconColor || "",
            iconAlt: n.iconAlt || n.label || "",
            items: n.items || [],
          },
        }));
        setNodes(gnodes);
        setEdges(data.edges || []);
      } catch (e) {
        console.error(e);
      }
    })();
  }, [mode, setNodes, setEdges]);

  useEffect(() => {
    const n = selection.nodes?.[0];
    const node = nodes.find((x) => x.id === n);
    const $ = (id) => document.getElementById(id);
    if (!node) {
      $("f-id").value = "";
      $("f-type").value = "connectorNode";
      $("f-label").value = "";
      $("f-desc").value = "";
      $("f-islug").value = "";
      $("f-icolor").value = "";
      $("f-ialt").value = "";
      $("f-items").value = "";
      return;
    }
    $("f-id").value = node.id;
    $("f-type").value = node.type;
    $("f-label").value = node.data.label || "";
    $("f-desc").value = node.data.description || "";
    $("f-islug").value = node.data.iconSlug || "";
    $("f-icolor").value = node.data.iconColor || "";
    $("f-ialt").value = node.data.iconAlt || "";
    $("f-items").value = (node.data.items || []).map((it) => `${it.slug},${it.name},${it.color||""}`).join("\n");
  }, [selection, nodes]);

  const onConnect = useCallback((params) => setEdges((eds) => addEdge({ ...params, animated: true, style: { stroke: "#3b82f6", strokeWidth: 3 } }, eds)), [setEdges]);

  const onSelectionChange = useCallback(({ nodes: ns, edges: es }) => setSelection({ nodes: ns.map((n) => n.id), edges: es.map((e) => e.id) }), []);

  // Hook up inspector inputs
  useEffect(() => {
    const $ = (id) => document.getElementById(id);
    function bind(id, handler) { const el = $(id); if (el) el.oninput = handler; }
    const modeSel = $("f-mode"); if (modeSel) modeSel.oninput = (e) => setMode(e.target.value);
    function updateSelected(mut) {
      setNodes((nds) => nds.map((n) => (selection.nodes.includes(n.id) ? mut({ ...n, data: { ...n.data } }) : n)));
    }
    bind("f-type", (e) => updateSelected((n) => (n.type = e.target.value, n.data.type = n.type, n)));
    bind("f-label", (e) => updateSelected((n) => (n.data.label = e.target.value, n)));
    bind("f-desc", (e) => updateSelected((n) => (n.data.description = e.target.value, n)));
    bind("f-islug", (e) => updateSelected((n) => (n.data.iconSlug = e.target.value, n)));
    bind("f-icolor", (e) => updateSelected((n) => (n.data.iconColor = e.target.value, n)));
    bind("f-ialt", (e) => updateSelected((n) => (n.data.iconAlt = e.target.value, n)));
    bind("f-items", (e) => updateSelected((n) => {
      const lines = e.target.value.split(/\r?\n/).map((l) => l.trim()).filter(Boolean);
      n.data.items = lines.map((l) => { const [slug,name,color] = l.split(','); return { slug: slug||"", name: name||"", color: color||"" }; });
      return n;
    }));
  }, [selection, setNodes]);

  // Buttons
  useEffect(() => {
    const $ = (id) => document.getElementById(id);
    $("btn-add").onclick = () => {
      const nextId = String(Math.max(0, ...nodes.map((n) => Number(n.id) || 0)) + 1);
      const nn = {
        id: nextId,
        type: "connectorNode",
        position: { x: 140, y: 140 },
        data: { label: "New Node", description: "", iconSlug: "", iconColor: "", iconAlt: "", items: [] },
      };
      setNodes((nds) => nds.concat(nn));
    };
    $("btn-del").onclick = () => {
      const ids = new Set(selection.nodes);
      setNodes((nds) => nds.filter((n) => !ids.has(n.id)));
      setEdges((eds) => eds.filter((e) => !(ids.has(e.source) || ids.has(e.target) || selection.edges.includes(e.id))));
    };
    $("btn-save-csv").onclick = () => {
      const nodeHeaders = ["id","type","x","y","label","description","iconSlug","iconColor","iconAlt"];
      const nodeRows = nodes.map((n) => ({ id:n.id, type:n.type, x:Math.round(n.position.x), y:Math.round(n.position.y), label:n.data.label||"", description:n.data.description||"", iconSlug:n.data.iconSlug||"", iconColor:n.data.iconColor||"", iconAlt:n.data.iconAlt||"" }));
      const edgeHeaders = ["id","source","target"];
      const edgeRows = edges.map((e,i) => ({ id:e.id || `e${i}`, source:e.source, target:e.target }));
      const itemHeaders = ["nodeId","slug","name","color"];
      const itemRows = nodes.flatMap((n) => (n.data.items||[]).map((it) => ({ nodeId:n.id, slug:it.slug, name:it.name, color:it.color||"" })));
      download("landing-nodes.csv", toCSV(nodeHeaders, nodeRows));
      download("landing-edges.csv", toCSV(edgeHeaders, edgeRows));
      download("landing-items.csv", toCSV(itemHeaders, itemRows));
    };
    $("btn-save-json").onclick = () => {
      const byId = new Map(nodes.map((n) => [n.id, n]));
      const existing = graph.nodes || [];
      const mergedNodes = Array.from(new Set([...existing.map(n=>n.id), ...nodes.map(n=>n.id)])).map((id) => {
        const old = existing.find((n) => n.id === id) || {};
        const cur = byId.get(id);
        const base = {
          id,
          type: cur?.type || old.type || "connectorNode",
          label: cur?.data.label ?? old.label ?? "",
          description: cur?.data.description ?? old.description ?? "",
          iconSlug: cur?.data.iconSlug ?? old.iconSlug ?? "",
          iconColor: cur?.data.iconColor ?? old.iconColor ?? "",
          iconAlt: cur?.data.iconAlt ?? old.iconAlt ?? "",
          items: cur?.data.items ?? old.items ?? [],
          posDesktop: old.posDesktop || { x: 140, y: 140 },
          posMobile: old.posMobile || { x: 140, y: 140 },
        };
        if (cur) {
          if (mode === "mobile") base.posMobile = { x: Math.round(cur.position.x), y: Math.round(cur.position.y) };
          else base.posDesktop = { x: Math.round(cur.position.x), y: Math.round(cur.position.y) };
        }
        return base;
      });
      const data = { nodes: mergedNodes, edges: edges.map((e, i) => ({ id: e.id || `e${i}`, source: e.source, target: e.target })) };
      download("flow-data.json", JSON.stringify(data, null, 2), "application/json");
    };
  }, [nodes, edges, selection, setNodes, setEdges]);

  return h(
    ReactFlow,
    {
      nodes: nodes.map((n) => ({ ...n, data: { ...n.data, type: n.type } })),
      edges,
      onNodesChange,
      onEdgesChange,
      onConnect,
      onSelectionChange,
      fitView: true,
      fitViewOptions: { padding: 0.2 },
      nodesDraggable: true,
      proOptions: { hideAttribution: true },
      nodeTypes,
      className: "bg-transparent",
    },
    h(Background, { variant: "dots" }),
    h(Controls, { position: "top-left" }),
  );
}

function mount() {
  const el = document.getElementById("rf-canvas-modifier");
  if (el) createRoot(el).render(h(Editor));
}
if (document.readyState === "loading") {
  window.addEventListener("DOMContentLoaded", mount);
} else {
  mount();
}
