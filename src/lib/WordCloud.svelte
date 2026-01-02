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
  let lastWidth = 0;

  function drawWordCloud() {
    if (!container || !svg) return;
    d3.select(svg).selectAll("*").remove();

    const topWords = words.slice(0, 20);

    const width = container.clientWidth;
    const height = container.clientHeight;

    d3.select(svg).attr("viewBox", `0 0 ${width} ${height}`);

    const maxCount = d3.max(topWords, (d) => d[1]) || 1;

    // Make font size range responsive
    const fontSizeRange = width < 768 ? [8, 50] : [10, 100];
    const sizeScale = d3.scaleSqrt().domain([0, maxCount]).range(fontSizeRange);

    const layout = cloud()
      .size([width, height])
      .words(
        topWords.map(
          (d) =>
            ({
              text: d[0],
              size: sizeScale(d[1]),
            }) as MyWord,
        ),
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
        .style("fill", (d, i) => d3.interpolatePlasma(i / 20))
        .attr("text-anchor", "middle")
        .attr("transform", (d) => `translate(${[d.x, d.y]})rotate(${d.rotate})`)
        .text((d) => d.text || "");
    }
  }

  function handleResize() {
    if (!container) return;
    const newWidth = container.clientWidth;
    if (newWidth !== lastWidth) {
      lastWidth = newWidth;
      drawWordCloud();
    }
  }

  onMount(() => {
    drawWordCloud();
    if (container) {
      lastWidth = container.clientWidth;
    }
  });
  $: if (words) drawWordCloud();
</script>

<svelte:window on:resize={handleResize} />

<div class="wordcloud-container h-full w-full" bind:this={container}>
  <svg bind:this={svg} style="width: 100%; height: 100%;" />
</div>
