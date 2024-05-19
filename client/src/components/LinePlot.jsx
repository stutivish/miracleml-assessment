import React, { useRef, useEffect, useState } from 'react';
import * as d3 from 'd3';

const BarChart = ({ data }) => {
    const svgRef = useRef();
    const [counts, setCounts] = useState([]);

    useEffect(() => {
        if (data && data.length) {
            const sponsorCounts = data.reduce((acc, curr) => {
                if (acc[curr.sponsor]) {
                    acc[curr.sponsor]++;
                } else {
                    acc[curr.sponsor] = 1;
                }
                return acc;
            }, {});

            const countsArray = Object.entries(sponsorCounts).map(([sponsor, count]) => ({ sponsor, count }));
            setCounts(countsArray);
        }
    }, [data]);

    useEffect(() => {
        if (counts && counts.length) {
            const margin = { top: 20, right: 30, bottom: 250, left: 60 };
            const width = 1200 - margin.left - margin.right;
            const height = 600 - margin.top - margin.bottom;

            const svg = d3.select(svgRef.current)
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
                .append("g")
                .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

            const xScale = d3.scaleBand()
                .domain(counts.map(d => d.sponsor))
                .range([0, width])
                .padding(0.1);

            const yScale = d3.scaleLinear()
                .domain([0, Math.ceil(d3.max(counts, d => d.count))])
                .range([height, 0]);

            svg.selectAll(".bar")
                .data(counts)
                .enter()
                .append("rect")
                .attr("class", "bar")
                .attr("x", d => xScale(d.sponsor))
                .attr("width", xScale.bandwidth())
                .attr("y", d => yScale(d.count))
                .attr("height", d => height - yScale(d.count));

            svg.append("g")
                .attr("transform", "translate(0," + height + ")")
                .call(d3.axisBottom(xScale))
                .selectAll("text")
                .attr("transform", "rotate(-45)")
                .style("text-anchor", "end")
                .text(function (d) {
                    return d.substring(0, 25);
                });

            svg.append("g")
                .call(d3.axisLeft(yScale));

            svg.append("text")
                .attr("transform", "rotate(-90)")
                .attr("y", 0 - margin.left)
                .attr("x", 0 - (height / 2))
                .attr("dy", "1em")
                .style("text-anchor", "middle")
                .text("Number of Trials");

            svg.append("text")
                .attr("x", width / 4)
                .attr("y", 0)
                .attr("text-anchor", "middle")
                .style("font-size", "16px")
                .text("Number of Trials by Sponsor");
        }
    }, [counts]);

    return <svg ref={svgRef}></svg>;
};

export default BarChart;