import * as d3 from "d3";

// export const categoryColors = new Map([
//     ["Nouns", "#1f77b4"],
//     ["Proper Nouns", "#2dbbd4"],
//     ["Verbs", "#ff7f0e"],
//     ["Adjectives", "#2ca02c"],
//     ["Adverbs", "#d62728"],
//     ["Adpositions", "#8c564b"],
//     ["Auxiliaries", "#e377c2"],
//     ["Numerals", "#7f7f7f"],
//     ["Interjections", "#bcbd22"],
//     ["Coordinating Conjunctions", "#991843"],
//     ["Determiners", "#ff9800"],
//     ["Subordinating Conjunctions", "#33754e"],
//     ["Other", "#383838"],
// ]);

export const categoryColors = new Map([
    ["Nouns", d3.interpolatePlasma(1 / 13)],
    ["Proper Nouns", d3.interpolatePlasma(6 / 13)],
    ["Verbs", d3.interpolatePlasma(10 / 13)],
    ["Adjectives", d3.interpolatePlasma(2 / 13)],
    ["Adverbs", d3.interpolatePlasma(9 / 13)],
    ["Adpositions", d3.interpolatePlasma(11 / 13)],
    ["Auxiliaries", d3.interpolatePlasma(4 / 13)],
    ["Numerals", d3.interpolatePlasma(10 / 13)],
    ["Interjections", d3.interpolatePlasma(5 / 13)],
    ["Coordinating Conjunctions", d3.interpolatePlasma(9 / 13)],
    ["Determiners", d3.interpolatePlasma(6 / 13)],
    ["Subordinating Conjunctions", d3.interpolatePlasma(8 / 13)],
    ["Other", d3.interpolatePlasma(7 / 13)],
]);
