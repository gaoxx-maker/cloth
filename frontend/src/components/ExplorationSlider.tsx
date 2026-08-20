"use client";
export function ExplorationSlider({value,onChange}:{value:number;onChange:(v:number)=>void}) { return <label>精准 <input aria-label="探索度" type="range" min="0" max="100" value={value} onChange={e=>onChange(+e.target.value)}/> 探索 {value}</label>; }
