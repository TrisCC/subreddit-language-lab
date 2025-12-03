<script lang="ts">
  import { onMount } from "svelte";
  import * as d3 from "d3";

  export let data: [string, number][];
  let svg: SVGSVGElement;
  let container: HTMLDivElement;

  function preprocessData(data: [string, number][]) {
    const total = data.reduce((sum, [, value]) => sum + value, 0);
    const main: [string, number][] = [];
    let otherSum = 0;
    for (const [cat, value] of data) {
      if (value / total <= 0.05) {
        otherSum += value;
      } else {
        main.push([cat, value]);
      }
    }
    if (otherSum > 0) {
      main.push(["Other", otherSum]);
    }
    return main;
  }

  onMount(() => {
    if (!container) return;

    const processedData = preprocessData(data);

    const width = container.clientWidth;
    const height = Math.min(width, 500);
    const radius = Math.min(width, height) / 2;

    d3.select(svg)
      .attr("width", width)
      .attr("height", height)
      .append("g")
      .attr("transform", `translate(${width / 2}, ${height / 2})`);

    const color = d3.scaleOrdinal(d3.schemeCategory10);

    const pie = d3.pie<[string, number]>().value((d) => d[1]);

    const arc = d3
      .arc<d3.PieArcDatum<[string, number]>>()
      .innerRadius(0)
      .outerRadius(radius);

    const g = d3.select(svg).select("g");

    const tooltip = d3
      .select(container)
      .append("div")
      .style("opacity", 0)
      .attr("class", "tooltip")
      .style("background-color", "white")
      .style("border", "solid")
      .style("border-width", "2px")
      .style("border-radius", "5px")
      .style("padding", "5px")
      .style("position", "absolute");

    const mouseover = function (
      this: SVGPathElement,
      event: MouseEvent,
      d: d3.PieArcDatum<[string, number]>
    ) {
      tooltip.style("opacity", 1);
      d3.select(this).style("stroke", "black").style("opacity", 1);
    };
    const mousemove = function (
      event: MouseEvent,
      d: d3.PieArcDatum<[string, number]>
    ) {
      tooltip
        .html(`${d.data[0]}: ${(d.data[1] * 100).toFixed(2)}%`)
        .style("left", `${event.pageX + 10}px`)
        .style("top", `${event.pageY}px`);
    };
    const mouseleave = function (
      this: SVGPathElement,
      event: MouseEvent,
      d: d3.PieArcDatum<[string, number]>
    ) {
      tooltip.style("opacity", 0);
      d3.select(this).style("stroke", "none").style("opacity", 0.8);
    };

    g.selectAll("path")
      .data(pie(processedData))
      .enter()
      .append("path")
      .attr("d", arc)
      .attr("fill", (d) => (d.data[0] === "Other" ? "#888" : color(d.data[0])))
      .style("opacity", 0.8)
      .on("mouseover", mouseover)
      .on("mousemove", mousemove)
      .on("mouseleave", mouseleave);

    const text = g
      .selectAll("text")
      .data(pie(processedData))
      .enter()
      .append("text")
      .attr("transform", (d) => `translate(${arc.centroid(d)})`)
      .style("text-anchor", "middle")
      .style("font-size", 15)
      .style("fill", "white");

    text.append("tspan").text((d) => d.data[0]);

    text
      .append("tspan")
      .attr("x", 0)
      .attr("dy", "1.2em")
      .text((d) => `${(d.data[1] * 100).toFixed(1)}%`);
  });
</script>

<div
  class="pie-chart-container"
  bind:this={container}
  style="position: relative;"
>
  <svg bind:this={svg} />
</div>
