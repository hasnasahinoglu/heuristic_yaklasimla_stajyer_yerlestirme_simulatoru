# ORİJİNAL AGAC (Detaylı gösterim)
# import json

# def generate_html_graph(all_states, best_state_id):
#     state_map = {s.id: s for s in all_states}
#     winning_path_ids = set()
#     curr = best_state_id
#     while curr is not None:
#         winning_path_ids.add(curr)
#         node = state_map.get(curr)
#         curr = node.parent_id if node else None
            
#     nodes = []
#     links = []
    
#     for s in all_states:
#         is_winner = s.id in winning_path_ids
#         color, radius, opacity, font_weight = "#6E6E6E", 6, 0.8, "normal"
#         text_color, label_text = "#555", f"{s.log_history} ({s.score:.0f})"
#         stroke = "#666"

#         if is_winner:
#             color, stroke = "#28a745", "#155724"
#             radius, opacity, font_weight = 10, 1.0, "bold"
#             text_color = "#000"
#             if s.id == best_state_id:
#                 color, radius = "#dc3545", 14
#                 label_text = f"🏁 FİNAL<br>📝 {s.log_history}<br>🏆 TOPLAM PUAN: {s.score:.2f}"

#         if "RED" in s.log_history:
#             color, stroke = "#D81B60", "#880E4F"
#             radius = 12
#         elif "TUR" in s.log_history: 
#             color, stroke, radius = "#ff9800", "#e65100", 9

#         nodes.append({
#             "id": s.id, "label": label_text, "color": color, 
#             "radius": radius, "stroke": stroke, "opacity": opacity,
#             "weight": font_weight, "text_color": text_color
#         })
        
#         if s.parent_id is not None:
#             is_link_winner = (s.id in winning_path_ids)
#             links.append({
#                 "source": s.parent_id, "target": s.id,
#                 "color": "#28a745" if is_link_winner else "#999",
#                 "width": 4 if is_link_winner else 1.5,
#                 "opacity": 1.0 if is_link_winner else 0.5
#             })

#     json_graph = json.dumps({"nodes": nodes, "links": links})
#     html_content = f"""
#     <!DOCTYPE html><html><head><meta charset="UTF-8">
#     <script src="https://d3js.org/d3.v7.min.js"></script>
#     <style>body{{font-family:'Segoe UI';background:#f8f9fa;margin:0;overflow:hidden}}#graph{{width:100vw;height:100vh}}.tooltip{{position:absolute;padding:10px;background:rgba(0,0,0,0.8);color:#fff;border-radius:5px;opacity:0;pointer-events:none;font-size:12px;line-height:1.4}}</style>
#     </head><body><div id="graph"></div><div class="tooltip" id="tooltip"></div>
#     <script>
#     const data={json_graph};
#     const width=window.innerWidth,height=window.innerHeight;
#     const svg=d3.select("#graph").append("svg").attr("width",width).attr("height",height).call(d3.zoom().on("zoom",e=>g.attr("transform",e.transform)));
#     const g=svg.append("g").attr("transform","translate(50,50)");
#     const root=d3.stratify().id(d=>d.id).parentId(d=>{{const l=data.links.find(x=>x.target===d.id);return l?l.source:null}})(data.nodes);
#     const tree=d3.tree().nodeSize([50,250]);tree(root);
#     g.selectAll(".link").data(root.links()).enter().append("path").attr("stroke",d=>d.target.data.color).attr("stroke-width",d=>d.target.data.width).attr("opacity",d=>d.target.data.opacity).attr("fill","none").attr("d",d3.linkVertical().x(d=>d.x).y(d=>d.y));
#     const node=g.selectAll(".node").data(root.descendants()).enter().append("g").attr("transform",d=>`translate(${{d.x}},${{d.y}})`);
#     node.append("circle").attr("r",d=>d.data.radius).attr("fill",d=>d.data.color).attr("stroke",d=>d.data.stroke).on("mouseover",(e,d)=>{{d3.select("#tooltip").style("opacity",1).html(d.data.label).style("left",(e.pageX+10)+"px").style("top",(e.pageY-20)+"px")}}).on("mouseout",()=>d3.select("#tooltip").style("opacity",0));
#     node.append("text").attr("dy","0.35em").attr("x",15).text(d=>d.data.label.split('<br>')[0].replace("📝 ", "")).style("font-weight",d=>d.data.weight).style("fill",d=>d.data.text_color).style("font-size","11px");
#     </script></body></html>
#     """
#     with open("beam_simulation_example.html", "w", encoding="utf-8") as f:
#         f.write(html_content)




# DOKUMAN ICIN CIZILEN AGAC (Yazısız)

import json

def generate_html_graph(all_states, best_state_id):
    state_map = {s.id: s for s in all_states}
    winning_path_ids = set()
    curr = best_state_id
    while curr is not None:
        winning_path_ids.add(curr)
        node = state_map.get(curr)
        curr = node.parent_id if node else None
            
    nodes = []
    links = []
    
    for s in all_states:
        is_winner = s.id in winning_path_ids
        
        # --- RENKLER ---
        color, radius, opacity = "#555555", 6, 0.9
        clean_log = str(s.log_history).strip().replace("\n", " ")
        label_text = f"📝 {clean_log}<br>📊 Puan: {s.score:.2f}"
        stroke = "#444"

        if is_winner:
            color, stroke = "#28a745", "#155724"
            radius, opacity = 9, 1.0
            if s.id == best_state_id:
                color, radius = "#9C27B0", 14
                label_text = f"🏁 <b>FİNAL SEÇİM</b><br>{label_text}"

        if "RED" in str(s.log_history) and s.id != best_state_id:
            color, stroke = "#D81B60", "#880E4F"
        elif "TUR" in str(s.log_history) and s.id != best_state_id: 
            color, stroke = "#ff9800", "#e65100"

        nodes.append({
            "id": s.id, "label": label_text, "color": color, 
            "radius": radius, "stroke": stroke, "opacity": opacity
        })
        
        if s.parent_id is not None:
            is_link_winner = (s.id in winning_path_ids)
            
            link_color = "#28a745" if is_link_winner else "#777"
            link_width = 3 if is_link_winner else 1.5
            link_opacity = 1.0 if is_link_winner else 0.6
            
            links.append({
                "source": s.parent_id, "target": s.id,
                "color": link_color,
                "width": link_width,
                "opacity": link_opacity
            })

    json_graph = json.dumps({"nodes": nodes, "links": links})
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Beam Search Visualization (Vertical)</title>
        <script src="https://d3js.org/d3.v7.min.js"></script>
        <style>
            body {{ background: #f8f9fa; margin: 0; overflow: hidden; }}
            #graph {{ width: 100vw; height: 100vh; }}
            .tooltip {{ 
                position: absolute; 
                padding: 10px; 
                background: rgba(0, 0, 0, 0.9); 
                color: #fff; 
                border-radius: 4px; 
                pointer-events: none; 
                font-family: sans-serif;
                font-size: 12px; 
                box-shadow: 0 4px 12px rgba(0,0,0,0.4);
                opacity: 0; 
                border: 1px solid #666;
                z-index: 100;
            }}
        </style>
    </head>
    <body>
        <div id="graph"></div>
        <div class="tooltip" id="tooltip"></div>
        <script>
            const data = {json_graph};
            const width = window.innerWidth;
            const height = window.innerHeight;

            const svg = d3.select("#graph").append("svg")
                .attr("width", width)
                .attr("height", height)
                .call(d3.zoom().scaleExtent([0.1, 5]).on("zoom", (e) => {{
                    g.attr("transform", e.transform);
                }}));

            const g = svg.append("g");

            const root = d3.stratify()
                .id(d => d.id)
                .parentId(d => {{
                    const l = data.links.find(x => x.target === d.id);
                    return l ? l.source : null;
                }})(data.nodes);

            // --- AYAR: DİKEY AĞAÇ DÜZENİ ---
            // nodeSize([yatay_genişlik, dikey_derinlik])
            // [30, 80]: Düğümler yan yana 30px, alt alta 80px mesafede.
            const treeLayout = d3.tree().nodeSize([30, 80]); 
            treeLayout(root);

            // --- AYAR: BAŞLANGIÇ KONUMU (Üst Orta) ---
            // translate(width / 2, 50): Ekranın ortasından ve 50px aşağıdan başla
            const initialTransform = d3.zoomIdentity.translate(width / 2, 50).scale(0.8);
            svg.call(d3.zoom().transform, initialTransform);

            // Linkler (Dikey Çizgiler - linkVertical)
            g.selectAll(".link")
                .data(root.links())
                .enter().append("path")
                .attr("fill", "none")
                .attr("stroke", d => {{
                    const targetLink = data.links.find(l => l.target === d.target.data.id);
                    return targetLink ? targetLink.color : "#999";
                }})
                .attr("stroke-width", d => {{
                    const targetLink = data.links.find(l => l.target === d.target.data.id);
                    return targetLink ? targetLink.width : 1;
                }})
                .attr("opacity", d => {{
                    const targetLink = data.links.find(l => l.target === d.target.data.id);
                    return targetLink ? targetLink.opacity : 0.5;
                }})
                // DİKEY MOD: x ve y normal yerinde
                .attr("d", d3.linkVertical().x(d => d.x).y(d => d.y));

            // Node'lar (Normal x, y koordinatları)
            const node = g.selectAll(".node")
                .data(root.descendants())
                .enter().append("g")
                .attr("transform", d => `translate(${{d.x}},${{d.y}})`);

            node.append("circle")
                .attr("r", d => d.data.radius)
                .attr("fill", d => d.data.color)
                .attr("stroke", d => d.data.stroke)
                .attr("stroke-width", 1.5)
                .style("cursor", "crosshair")
                .on("mouseover", (e, d) => {{
                    d3.select("#tooltip")
                        .style("opacity", 1)
                        .html(d.data.label)
                        .style("left", (e.pageX + 15) + "px")
                        .style("top", (e.pageY - 15) + "px");
                    
                    d3.select(e.target)
                        .attr("stroke", "#fff")
                        .attr("stroke-width", 3)
                        .attr("r", d.data.radius + 2);
                }})
                .on("mouseout", (e, d) => {{
                    d3.select("#tooltip").style("opacity", 0);
                    d3.select(e.target)
                        .attr("stroke", d.data.stroke)
                        .attr("stroke-width", 1.5)
                        .attr("r", d.data.radius);
                }});
        </script>
    </body>
    </html>
    """
    
    with open("beam_simulation_example.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print("Graph generated (Vertical Mode): beam_simulation_example.html")