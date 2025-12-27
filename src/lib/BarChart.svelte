<script lang="ts">
  import { onMount } from "svelte";
  import * as d3 from "d3";

  export let data: [string, number][];
  let svg: SVGSVGElement;
  let container: HTMLDivElement;

  function drawChart() {
    if (!container || !svg) return;
    d3.select(svg).selectAll("*").remove();

    const longestLabelLength =
      data.length > 0 ? Math.max(...data.map((d) => d[0].length)) : 0;
    const dynamicLeftMargin = longestLabelLength * 8 + 20;

    const margin = {
      top: 20,
      right: 30,
      bottom: 40,
      left: Math.max(100, dynamicLeftMargin),
    };
    const width = container.clientWidth;
    const height = Math.max(320, data.length * 28 + margin.top + margin.bottom);

    d3.select(svg).attr("width", width).attr("height", height);

    const chartWidth = width - margin.left - margin.right;
    if (chartWidth <= 0) return;
    const chartHeight = height - margin.top - margin.bottom;

    const x = d3
      .scaleLinear()
      .domain([0, d3.max(data, (d) => d[1]) || 1])
      .range([0, chartWidth]);

    const y = d3
      .scaleBand()
      .domain(data.map((d) => d[0]))
      .range([0, chartHeight])
      .padding(0.2);

    const g = d3
      .select(svg)
      .append("g")
      .attr("transform", `translate(${margin.left},${margin.top})`);

    g.append("g")
      .call(d3.axisLeft(y))
      .selectAll("text")
      .style("font-size", "14px");

    g.append("g")
      .attr("transform", `translate(0,${chartHeight})`)
      .call(d3.axisBottom(x).ticks(5))
      .selectAll("text")
      .style("font-size", "14px");

    g.selectAll("rect")
      .data(data)
      .enter()
      .append("rect")
      .attr("y", (d) => y(d[0])!)
      .attr("x", 0)
      .attr("height", y.bandwidth())
      .attr("width", (d) => x(d[1]))
      .attr("fill", "#3b82f6");

    g.selectAll("text.bar-label")
      .data(data)
      .enter()
      .append("text")
      .attr("class", "bar-label")
      .attr("x", (d) => x(d[1]) + 5)
      .attr("y", (d) => y(d[0])! + y.bandwidth() / 2)
      .attr("dy", "0.35em")
      .text((d) => d[1])
      .style("font-size", "13px")
      .style("fill", "#333");
  }

  onMount(drawChart);
  $: if (data) drawChart();
</script>

<svelte:window on:resize={drawChart} />

<div class="bar-chart-container" bind:this={container}>
  <svg bind:this={svg} style="width: 100%; height: auto;" />
</div>
