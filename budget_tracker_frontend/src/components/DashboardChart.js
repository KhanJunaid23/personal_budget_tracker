import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';

const DashboardChart = ({ income, expenses }) => {
  const chartRef = useRef();

  useEffect(() => {
    d3.select(chartRef.current).selectAll('*').remove(); // Clear old chart

    const data = [
      { label: 'Income', value: income },
      { label: 'Expenses', value: expenses },
    ];

    const width = 300;
    const height = 300;
    const radius = Math.min(width, height) / 2;

    const color = d3.scaleOrdinal().range(['#28a745', '#dc3545']);

    const svg = d3
      .select(chartRef.current)
      .append('svg')
      .attr('width', width)
      .attr('height', height)
      .append('g')
      .attr('transform', `translate(${width / 2},${height / 2})`);

    const pie = d3.pie().value((d) => d.value);
    const data_ready = pie(data);

    const arc = d3.arc().innerRadius(60).outerRadius(radius);

    svg
      .selectAll('slices')
      .data(data_ready)
      .enter()
      .append('path')
      .attr('d', arc)
      .attr('fill', (d) => color(d.data.label))
      .style('stroke', '#fff')
      .style('stroke-width', '2px');

    svg
      .selectAll('text')
      .data(data_ready)
      .enter()
      .append('text')
      .text((d) => `${d.data.label} (${d.data.value})`)
      .attr('transform', (d) => `translate(${arc.centroid(d)})`)
      .style('text-anchor', 'middle')
      .style('font-size', '12px')
      .style('fill', '#fff');
  }, [income, expenses]);

  return <div ref={chartRef}></div>;
};

export default DashboardChart;
