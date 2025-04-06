import React, { useRef, useEffect } from 'react';
import * as d3 from 'd3';

const BudgetChart = ({ budget, expenses }) => {
  const chartRef = useRef();

  useEffect(() => {
    if (budget === undefined || expenses === undefined) return;

    d3.select(chartRef.current).selectAll('*').remove();
    const width = 400;
    const height = 300;
    const margin = { top: 20, right: 30, bottom: 40, left: 40 };

    const svg = d3.select(chartRef.current)
      .append('svg')
      .attr('width', width)
      .attr('height', height);
    const x = d3.scaleBand()
      .domain(['Budget', 'Expenses'])
      .range([margin.left, width - margin.right])
      .padding(0.2);
    const y = d3.scaleLinear()
      .domain([0, Math.max(budget, expenses) * 1.2])
      .range([height - margin.bottom, margin.top]);

    svg.append('g')
      .selectAll('rect')
      .data([{ label: 'Budget', value: budget }, { label: 'Expenses', value: expenses }])
      .join('rect')
      .attr('x', d => x(d.label))
      .attr('y', d => y(d.value))
      .attr('height', d => y(0) - y(d.value))
      .attr('width', x.bandwidth())
      .attr('fill', d => d.label === 'Budget' ? '#4e73df' : '#e74a3b');

    svg.append('g')
      .attr('transform', `translate(0,${height - margin.bottom})`)
      .call(d3.axisBottom(x));

    svg.append('g')
      .attr('transform', `translate(${margin.left},0)`)
      .call(d3.axisLeft(y));

    svg.append('text')
      .attr('x', width / 2)
      .attr('y', margin.top)
      .attr('text-anchor', 'middle')
      .style('font-size', '16px')
      .text('Budget vs Expenses');

    svg.append('g')
      .selectAll('text')
      .data([{ label: 'Budget', value: budget }, { label: 'Expenses', value: expenses }])
      .join('text')
      .attr('x', d => x(d.label) + x.bandwidth() / 2)
      .attr('y', d => y(d.value) - 5)
      .attr('text-anchor', 'middle')
      .text(d => `₹${d.value.toLocaleString()}`);

  }, [budget, expenses]);

  return <div ref={chartRef} />;
};

export default BudgetChart;