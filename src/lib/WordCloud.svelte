<script lang="ts">
  import { onMount } from "svelte";
  import * as d3 from "d3";
  import cloud, { type Word } from "d3-cloud";

  interface MyWord extends Word {
    text: string;
    size: number;
  }

  export let words: [string, number][];
  let svg: SVGSVGElement;
  let container: HTMLDivElement;

  function drawWordCloud() {
    if (!container || !svg) return;
    d3.select(svg).selectAll("*").remove();

    const width = container.clientWidth;
    const height = Math.round(width * 0.66);

    d3.select(svg).attr("viewBox", `0 0 ${width} ${height}`);

    const maxCount = d3.max(words, (d) => d[1]) || 1;
    const sizeScale = d3.scaleSqrt().domain([0, maxCount]).range([10, 100]);

    const layout = cloud()
      .size([width, height])
      .words(
        words.map(
          (d) =>
            ({
              text: d[0],
              size: sizeScale(d[1]),
            }) as MyWord
        )
      )
      .padding(5)
      .rotate(0)
      .font("Impact")
      .fontSize((d) => d.size || 0)
      .on("end", draw);

    layout.start();

    function draw(words: Word[]) {
      d3.select(svg)
        .append("g")
        .attr("transform", `translate(${width / 2},${height / 2})`)
        .selectAll("text")
        .data(words)
        .enter()
        .append("text")
        .style("font-size", (d) => `${d.size}px`)
        .style("font-family", "Impact")
        .style("fill", (d, i) => d3.schemeCategory10[i % 10])
        .attr("text-anchor", "middle")
        .attr("transform", (d) => `translate(${[d.x, d.y]})rotate(${d.rotate})`)
        .text((d) => d.text || "");
    }
  }

  onMount(drawWordCloud);
  $: if (words) drawWordCloud();
</script>

<div class="wordcloud-container" bind:this={container}>
  <svg bind:this={svg} style="width: 100%; height: 350px;" />
</div>
