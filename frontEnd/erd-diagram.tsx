"use client"

import { useMemo } from "react"

interface Attribute {
  name: string
  type: string
  primaryKey?: boolean
  foreignKey?: boolean
}

interface Entity {
  name: string
  columns?: Attribute[]
  attributes?: Attribute[]
}

interface Relationship {
  type: string
  from: string
  to: string
  fromColumn?: string
  toColumn?: string
}

interface ERDData {
  entities: Entity[]
  relationships: Relationship[]
}

interface ERDDiagramProps {
  erdData: ERDData
}

const EntityBox = ({
  entity,
  position,
  color,
}: { entity: Entity; position: { x: number; y: number }; color: string }) => {
  const attributes = entity.columns || entity.attributes || []

  const colorClasses = {
    blue: "bg-blue-500 border-blue-600",
    red: "bg-red-500 border-red-600",
    pink: "bg-pink-500 border-pink-600",
    green: "bg-green-500 border-green-600",
    purple: "bg-purple-500 border-purple-600",
  }

  return (
    <div
      className="absolute bg-white border-2 rounded-lg shadow-lg min-w-[200px] max-w-[250px]"
      style={{ left: position.x, top: position.y }}
    >
      {/* Entity Header */}
      <div className={`${colorClasses[color]} text-white px-4 py-2 rounded-t-lg`}>
        <h3 className="font-bold text-sm text-center">{entity.name}</h3>
      </div>

      {/* Attributes List */}
      <div className="p-3 max-h-[300px] overflow-y-auto">
        {attributes.map((attr, index) => (
          <div
            key={index}
            className="flex justify-between items-center py-1 text-xs border-b border-gray-100 last:border-b-0"
          >
            <div className="flex items-center gap-1">
              {attr.primaryKey && <span className="text-yellow-600 font-bold">🔑</span>}
              {attr.foreignKey && <span className="text-blue-600 font-bold">🔗</span>}
              <span
                className={`font-medium ${attr.primaryKey ? "text-yellow-700" : attr.foreignKey ? "text-blue-700" : "text-gray-700"}`}
              >
                {attr.name}
              </span>
            </div>
            <span className="text-gray-500 text-xs">{attr.type}</span>
          </div>
        ))}
      </div>
    </div>
  )
}

const RelationshipLine = ({
  from,
  to,
  type,
  fromPos,
  toPos,
}: {
  from: string
  to: string
  type: string
  fromPos: { x: number; y: number }
  toPos: { x: number; y: number }
}) => {
  // Calculate connection points (center of entity boxes)
  const fromX = fromPos.x + 125 // Half of entity width
  const fromY = fromPos.y + 50 // Approximate center height
  const toX = toPos.x + 125
  const toY = toPos.y + 50

  // Create path for the connection line
  const pathData = `M ${fromX} ${fromY} L ${toX} ${toY}`

  return (
    <g>
      <path d={pathData} stroke="#6b7280" strokeWidth="2" fill="none" markerEnd="url(#arrowhead)" />
      {/* Relationship label */}
      <text
        x={(fromX + toX) / 2}
        y={(fromY + toY) / 2 - 10}
        textAnchor="middle"
        className="text-xs fill-gray-600 font-medium"
      >
        {type}
      </text>
    </g>
  )
}

export default function ERDDiagram({ erdData }: ERDDiagramProps) {
  const { entities, relationships } = erdData

  // Calculate positions for entities in a grid-like layout
  const entityPositions = useMemo(() => {
    const positions = {}
    const colors = ["blue", "red", "pink", "green", "purple"]

    entities.forEach((entity, index) => {
      const row = Math.floor(index / 3)
      const col = index % 3
      positions[entity.name] = {
        x: col * 280 + 50,
        y: row * 350 + 50,
        color: colors[index % colors.length],
      }
    })

    return positions
  }, [entities])

  // Calculate diagram dimensions
  const maxX = Math.max(...Object.values(entityPositions).map((pos) => pos.x)) + 250
  const maxY = Math.max(...Object.values(entityPositions).map((pos) => pos.y)) + 300

  return (
    <div className="w-full bg-slate-50 border rounded-lg p-4 overflow-auto">
      <div className="relative" style={{ width: Math.max(maxX, 800), height: Math.max(maxY, 600) }}>
        {/* SVG for relationship lines */}
        <svg className="absolute inset-0 pointer-events-none" width="100%" height="100%">
          <defs>
            <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
              <polygon points="0 0, 10 3.5, 0 7" fill="#6b7280" />
            </marker>
          </defs>

          {/* Render relationship lines */}
          {relationships.map((rel, index) => {
            const fromPos = entityPositions[rel.from]
            const toPos = entityPositions[rel.to]

            if (!fromPos || !toPos) return null

            return (
              <RelationshipLine
                key={index}
                from={rel.from}
                to={rel.to}
                type={rel.type}
                fromPos={fromPos}
                toPos={toPos}
              />
            )
          })}
        </svg>

        {/* Render entity boxes */}
        {entities.map((entity, index) => {
          const position = entityPositions[entity.name]
          if (!position) return null

          return <EntityBox key={entity.name} entity={entity} position={position} color={position.color} />
        })}
      </div>

      {/* Legend */}
      <div className="mt-6 p-4 bg-white rounded-lg border">
        <h4 className="font-semibold text-sm mb-3 text-gray-700">Legend</h4>
        <div className="flex flex-wrap gap-4 text-xs">
          <div className="flex items-center gap-2">
            <span className="text-yellow-600">🔑</span>
            <span>Primary Key</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-blue-600">🔗</span>
            <span>Foreign Key</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-2 bg-gray-400"></div>
            <span>Relationship</span>
          </div>
        </div>
      </div>
    </div>
  )
}
