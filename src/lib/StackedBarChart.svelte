<script lang="ts">
  import { onMount } from "svelte";
  import * as d3 from "d3";
  import { categoryColors } from "./colors";

  export let data: Record<string, Record<string, number>>; // {category: {length: count}}
  export let categories: string[] = ["Nouns", "Verbs", "Adjectives", "Adverbs"];

  const colors = categories.map((c) => categoryColors.get(c)!);

  let svg: SVGSVGElement;
  let container: HTMLDivElement;

  function safeCategory(cat: string) {
    return data[cat.toLowerCase()] || {};
  }

  function drawStackedBarChart() {
    if (!container || !svg) return;
    d3.select(svg).selectAll("*").remove();
    const margin = { top: 20, right: 30, bottom: 60, left: 50 };
    const width = container.clientWidth;
    const height = 300;

    d3.select(svg).attr("width", width).attr("height", height);

    // Get all word lengths
    const lengths = Array.from(
      new Set(categories.flatMap((cat) => Object.keys(safeCategory(cat)))),
    )
      .map(Number)
      .sort((a, b) => a - b);

    // Prepare stacked data
    const stackData = lengths.map((len) => {
      const entry: any = { length: len };
      categories.forEach((cat, i) => {
        entry[cat] = safeCategory(cat)[len] || 0;
      });
      return entry;
    });

    const stack = d3
      .stack()
      .keys(categories)
      .order(d3.stackOrderNone)
      .offset(d3.stackOffsetNone);

    const series = stack(stackData);

    const x = d3
      .scaleBand()
      .domain(lengths.map(String))
      .range([margin.left, width - margin.right])
      .padding(0.2);

    const y = d3
      .scaleLinear()
      .domain([
        0,
        d3.max(stackData, (d) =>
          categories.reduce((sum, cat) => sum + d[cat], 0),
        ) || 1,
      ])
      .nice()
      .range([height - margin.bottom, margin.top]);

    const g = d3.select(svg).append("g");

    // Draw bars
    series.forEach((catSeries, i) => {
      g.selectAll(`rect.cat-${i}`)
        .data(catSeries)
        .enter()
        .append("rect")
        .attr("x", (d) => x(String(d.data.length))!)
        .attr("y", (d) => y(d[1]))
        .attr("height", (d) => y(d[0]) - y(d[1]))
        .attr("width", x.bandwidth())
        .attr("fill", colors[i]);
    });

    // X axis
    g.append("g")
      .attr("transform", `translate(0,${height - margin.bottom})`)
      .call(d3.axisBottom(x))
      .selectAll("text")
      .style("font-size", "13px");

    // Y axis
    g.append("g")
      .attr("transform", `translate(${margin.left},0)`)
      .call(d3.axisLeft(y))
      .selectAll("text")
      .style("font-size", "13px");

    // Legend
    const legend = g
      .append("g")
      .attr(
        "transform",
        `translate(${width / 2 - (categories.length * 50) / 2},${height - margin.bottom + 30})`,
      );
    categories.forEach((cat, i) => {
      const legendItem = legend
        .append("g")
        .attr("transform", `translate(${i * 100},0)`);
      legendItem
        .append("rect")
        .attr("width", 18)
        .attr("height", 18)
        .attr("fill", colors[i]);
      legendItem
        .append("text")
        .attr("x", 24)
        .attr("y", 14)
        .text(cat)
        .style("font-size", "15px");
    });
  }

  onMount(drawStackedBarChart);
  $: if (data) drawStackedBarChart();
</script>

<svelte:window on:resize={drawStackedBarChart} />

<div class="stacked-bar-chart-container" bind:this={container}>
  <svg bind:this={svg} style="width: 100%; height: auto;" />
</div>
