// "use client"

// import { useState } from "react"
// import { Button } from "@/components/ui/button"
// import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
// import { Input } from "@/components/ui/input"
// import { Label } from "@/components/ui/label"
// import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
// import { Switch } from "@/components/ui/switch"
// import { Textarea } from "@/components/ui/textarea"
// import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "@/components/ui/collapsible"
// import { ChevronDown, Upload, Loader2, FileText, Database, Sparkles, BarChart3, AlertCircle } from "lucide-react"
// import ERDDiagram from "./erd-diagram"

// // Utility function to generate Mermaid ERD syntax
// function generateMermaid(erd_json) {
//   if (!erd_json || !erd_json.entities) return ""

//   const lines = ["erDiagram"]

//   // Add relationships
//   erd_json.relationships?.forEach((r) => {
//     const rel = r.type === "one-to-many" ? "||--o{" : "||--||"
//     lines.push(`    ${r.from.toUpperCase()} ${rel} ${r.to.toUpperCase()} : relates`)
//   })

//   // Add entities
//   ;(erd_json.entities || []).forEach((entity) => {
//     lines.push(`    ${entity.name.toUpperCase()} {`)
//     const attrs = entity.attributes || entity.columns || []
//     attrs.forEach((attr) => {
//       const keyIndicator = attr.primaryKey ? " PK" : attr.foreignKey ? " FK" : ""
//       lines.push(`        ${attr.type} ${attr.name}${keyIndicator}`)
//     })
//     lines.push("    }")
//   })

//   return lines.join("\n")
// }

// export default function ERDGenerator() {
//   const [formData, setFormData] = useState({
//     model_type: "",
//     business_requirement: "",
//     erp_system_name: "",
//     fantasy_mode: false,
//     excel_file: null,
//   })

//   const [response, setResponse] = useState(null)
//   const [loading, setLoading] = useState(false)
//   const [error, setError] = useState(null)
//   const [jsonCollapsed, setJsonCollapsed] = useState(true)

//   const handleInputChange = (field, value) => {
//     setFormData((prev) => ({ ...prev, [field]: value }))
//     // Clear error when user starts typing
//     if (error) setError(null)
//   }

//   const handleFileChange = (e) => {
//     const file = e.target.files?.[0]
//     setFormData((prev) => ({ ...prev, excel_file: file }))
//     if (error) setError(null)
//   }

//   const handleSubmit = async (e) => {
//     e.preventDefault()
//     setLoading(true)
//     setError(null)

//     try {
//       // Create FormData for multipart/form-data submission
//       const formDataToSend = new FormData()

//       // Add form fields
//       formDataToSend.append("model_type", formData.model_type)
//       formDataToSend.append("business_requirement", formData.business_requirement)
//       formDataToSend.append("erp_system_name", formData.erp_system_name)
//       formDataToSend.append("fantasy_mode", formData.fantasy_mode.toString())

//       // Add file if present
//       if (formData.excel_file) {
//         formDataToSend.append("file", formData.excel_file)
//       }

//       // Make POST request to /generate-erd
//       const apiResponse = await fetch("http://localhost:8000/generate-erd", {
//         method: "POST",
//         body: formDataToSend,
//       })

//       if (!apiResponse.ok) {
//         const errorData = await apiResponse.json().catch(() => ({}))
//         throw new Error(errorData.message || `HTTP error! status: ${apiResponse.status}`)
//       }

//       const responseData = await apiResponse.json()

//       // Update state with actual response data
//       setResponse(responseData)
//     } catch (error) {
//       console.error("Error generating ERD:", error)
//       setError(error.message)
//     } finally {
//       setLoading(false)
//     }
//   }

//   const mermaidCode = response?.erd_json ? generateMermaid(response.erd_json) : ""

//   return (
//     <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 p-4">
//       <div className="max-w-7xl mx-auto space-y-8">
//         {/* Header */}
//         <div className="text-center space-y-4">
//           <div className="flex items-center justify-center gap-3">
//             <Database className="w-8 h-8 text-blue-600" />
//             <h1 className="text-4xl font-bold text-slate-800">ERD Schema Generator</h1>
//           </div>
//           <p className="text-slate-600 text-lg max-w-2xl mx-auto">
//             Generate Entity Relationship Diagrams from your business requirements and data structures
//           </p>
//         </div>

//         {/* Error Display */}
//         {error && (
//           <Card className="shadow-lg border-red-200">
//             <CardContent className="p-6">
//               <div className="flex items-center gap-3 text-red-700">
//                 <AlertCircle className="w-5 h-5" />
//                 <div>
//                   <h3 className="font-semibold">Error Generating ERD</h3>
//                   <p className="text-sm text-red-600">{error}</p>
//                 </div>
//               </div>
//             </CardContent>
//           </Card>
//         )}

//         <div className="grid lg:grid-cols-2 gap-8">
//           {/* Configuration Section */}
//           <div className="space-y-6">
//             <Card className="shadow-lg">
//               <CardHeader className="bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-t-lg">
//                 <CardTitle className="flex items-center gap-2">
//                   <FileText className="w-5 h-5" />
//                   Configuration
//                 </CardTitle>
//                 <CardDescription className="text-blue-100">Configure your ERD generation parameters</CardDescription>
//               </CardHeader>
//               <CardContent className="p-6 space-y-6">
//                 <form onSubmit={handleSubmit} className="space-y-6">
//                   {/* Model Type */}
//                   <div className="space-y-2">
//                     <Label htmlFor="model_type" className="text-sm font-medium">
//                       Model Type
//                     </Label>
//                     <Select
//                       value={formData.model_type}
//                       onValueChange={(value) => handleInputChange("model_type", value)}
//                     >
//                       <SelectTrigger>
//                         <SelectValue placeholder="Select model type" />
//                       </SelectTrigger>
//                       <SelectContent>
//                         <SelectItem value="erp-based">ERP-based</SelectItem>
//                         <SelectItem value="generic">Generic</SelectItem>
//                       </SelectContent>
//                     </Select>
//                   </div>

//                   {/* Business Requirements */}
//                   <div className="space-y-2">
//                     <Label htmlFor="business_requirement" className="text-sm font-medium">
//                       Business Requirements
//                     </Label>
//                     <Textarea
//                       id="business_requirement"
//                       placeholder="Describe your business requirements and data relationships..."
//                       value={formData.business_requirement}
//                       onChange={(e) => handleInputChange("business_requirement", e.target.value)}
//                       className="min-h-[120px] resize-none"
//                     />
//                   </div>

//                   {/* ERP System Name */}
//                   <div className="space-y-2">
//                     <Label htmlFor="erp_system_name" className="text-sm font-medium">
//                       ERP System Name (Optional)
//                     </Label>
//                     <Input
//                       id="erp_system_name"
//                       placeholder="e.g., SAP, Oracle, Dynamics 365"
//                       value={formData.erp_system_name}
//                       onChange={(e) => handleInputChange("erp_system_name", e.target.value)}
//                     />
//                   </div>

//                   {/* Fantasy Mode Toggle */}
//                   <div className="flex items-center justify-between p-4 bg-slate-50 rounded-lg">
//                     <div className="space-y-1">
//                       <Label htmlFor="fantasy_mode" className="text-sm font-medium flex items-center gap-2">
//                         <Sparkles className="w-4 h-4 text-purple-600" />
//                         Fantasy Mode
//                       </Label>
//                       <p className="text-xs text-slate-600">Generate additional creative entities</p>
//                     </div>
//                     <Switch
//                       id="fantasy_mode"
//                       checked={formData.fantasy_mode}
//                       onCheckedChange={(checked) => handleInputChange("fantasy_mode", checked)}
//                     />
//                   </div>

//                   {/* File Upload */}
//                   <div className="space-y-2">
//                     <Label htmlFor="excel_file" className="text-sm font-medium">
//                       Excel File Upload
//                     </Label>
//                     <div className="border-2 border-dashed border-slate-300 rounded-lg p-6 text-center hover:border-slate-400 transition-colors">
//                       <Upload className="w-8 h-8 text-slate-400 mx-auto mb-2" />
//                       <Input
//                         id="excel_file"
//                         type="file"
//                         accept=".xlsx,.xls"
//                         onChange={handleFileChange}
//                         className="hidden"
//                       />
//                       <Label htmlFor="excel_file" className="cursor-pointer">
//                         <span className="text-sm text-slate-600">
//                           {formData.excel_file ? formData.excel_file.name : "Click to upload Excel file"}
//                         </span>
//                         <p className="text-xs text-slate-500 mt-1">Columns: Table Name, Column Name</p>
//                       </Label>
//                     </div>
//                   </div>

//                   {/* Submit Button */}
//                   <Button
//                     type="submit"
//                     className="w-full bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800"
//                     disabled={loading}
//                   >
//                     {loading ? (
//                       <>
//                         <Loader2 className="w-4 h-4 mr-2 animate-spin" />
//                         Generating ERD...
//                       </>
//                     ) : (
//                       "Generate ERD"
//                     )}
//                   </Button>
//                 </form>
//               </CardContent>
//             </Card>
//           </div>

//           {/* Results Section - Always Visible */}
//           <div className="space-y-6">
//             {/* Analysis Summary */}
//             <Card className="shadow-lg">
//               <CardHeader className="bg-gradient-to-r from-green-600 to-green-700 text-white rounded-t-lg">
//                 <CardTitle className="flex items-center gap-2">
//                   <BarChart3 className="w-5 h-5" />
//                   Analysis Summary
//                 </CardTitle>
//               </CardHeader>
//               <CardContent className="p-6">
//                 {response?.summary ? (
//                   <div className="prose prose-sm max-w-none">
//                     <pre className="whitespace-pre-wrap text-sm text-slate-700 font-sans leading-relaxed">
//                       {response.summary}
//                     </pre>
//                   </div>
//                 ) : (
//                   <div className="text-center py-12 text-slate-500">
//                     <BarChart3 className="w-12 h-12 mx-auto mb-4 text-slate-300" />
//                     <p className="text-lg font-medium mb-2">No Analysis Yet</p>
//                     <p className="text-sm">Generate an ERD to see the analysis summary here</p>
//                   </div>
//                 )}
//               </CardContent>
//             </Card>

//             {/* ERD JSON Data */}
//             <Card className="shadow-lg">
//               <Collapsible open={!jsonCollapsed} onOpenChange={setJsonCollapsed}>
//                 <CollapsibleTrigger asChild>
//                   <CardHeader className="bg-gradient-to-r from-purple-600 to-purple-700 text-white rounded-t-lg cursor-pointer hover:from-purple-700 hover:to-purple-800 transition-colors">
//                     <CardTitle className="flex items-center justify-between">
//                       <span className="flex items-center gap-2">
//                         <Database className="w-5 h-5" />
//                         ERD JSON Data
//                       </span>
//                       <ChevronDown className={`w-5 h-5 transition-transform ${!jsonCollapsed ? "rotate-180" : ""}`} />
//                     </CardTitle>
//                   </CardHeader>
//                 </CollapsibleTrigger>
//                 <CollapsibleContent>
//                   <CardContent className="p-6">
//                     {response?.erd_json ? (
//                       <pre className="bg-slate-100 p-4 rounded-lg text-xs overflow-auto max-h-96">
//                         {JSON.stringify(response.erd_json, null, 2)}
//                       </pre>
//                     ) : (
//                       <div className="text-center py-8 text-slate-500">
//                         <Database className="w-8 h-8 mx-auto mb-3 text-slate-300" />
//                         <p className="text-sm">JSON data will appear here after generation</p>
//                       </div>
//                     )}
//                   </CardContent>
//                 </CollapsibleContent>
//               </Collapsible>
//             </Card>

//             {/* Fantasy Entities - Only show when fantasy mode is enabled */}
//             {formData.fantasy_mode && (
//               <Card className="shadow-lg border-purple-200">
//                 <CardHeader className="bg-gradient-to-r from-purple-100 to-purple-200">
//                   <CardTitle className="flex items-center gap-2 text-purple-800">
//                     <Sparkles className="w-5 h-5" />
//                     Fantasy Entities
//                   </CardTitle>
//                 </CardHeader>
//                 <CardContent className="p-6">
//                   {response?.fantasy_entities ? (
//                     <div className="space-y-4">
//                       {response.fantasy_entities.map((entity, index) => (
//                         <div key={index} className="bg-purple-50 p-4 rounded-lg">
//                           <h4 className="font-semibold text-purple-800 mb-2">{entity.name}</h4>
//                           <div className="space-y-1">
//                             {(entity.attributes || []).map((attr, attrIndex) => (
//                               <div key={attrIndex} className="text-sm text-purple-700">
//                                 <span className="font-mono">{attr.name}</span>
//                                 <span className="text-purple-600"> ({attr.type})</span>
//                                 {attr.primary_key && <span className="text-purple-800 font-semibold"> PK</span>}
//                               </div>
//                             ))}
//                           </div>
//                         </div>
//                       ))}
//                     </div>
//                   ) : (
//                     <div className="text-center py-8 text-purple-500">
//                       <Sparkles className="w-8 h-8 mx-auto mb-3 text-purple-300" />
//                       <p className="text-sm">Fantasy entities will appear here after generation</p>
//                     </div>
//                   )}
//                 </CardContent>
//               </Card>
//             )}
//           </div>
//         </div>

//         {/* Entity Relationship Diagram - Always Visible */}
//         <Card className="shadow-lg">
//           <CardHeader className="bg-gradient-to-r from-indigo-600 to-indigo-700 text-white rounded-t-lg">
//             <CardTitle className="flex items-center gap-2">
//               <Database className="w-5 h-5" />
//               Entity Relationship Diagram
//             </CardTitle>
//           </CardHeader>
//           <CardContent className="p-6">
//             {response?.erd_json ? (
//               <ERDDiagram erdData={response.erd_json} />
//             ) : (
//               <div className="text-center py-16 text-slate-500">
//                 <Database className="w-16 h-16 mx-auto mb-4 text-slate-300" />
//                 <p className="text-xl font-medium mb-2">No Diagram Generated</p>
//                 <p className="text-sm">Your Entity Relationship Diagram will appear here after generation</p>
//               </div>
//             )}
//           </CardContent>
//         </Card>
//       </div>
//     </div>
//   )
// }

"use client"

import type React from "react"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Switch } from "@/components/ui/switch"
import { Textarea } from "@/components/ui/textarea"
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "@/components/ui/collapsible"
import { ChevronDown, Upload, Loader2, FileText, Database, Sparkles, BarChart3, AlertCircle } from "lucide-react"
import ERDDiagram from "./erd-diagram"

// Type definitions
interface Attribute {
  name: string
  type: string
  primaryKey?: boolean
  foreignKey?: boolean
  primary_key?: boolean
  foreign_key?: boolean
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

interface APIResponse {
  summary?: string
  erd_json?: ERDData
  fantasy_entities?: Entity[]
}

// Utility function to generate Mermaid ERD syntax
function generateMermaid(erd_json: ERDData | undefined): string {
  if (!erd_json || !erd_json?.entities) return ""

  const lines = ["erDiagram"]

  // Add relationships
  erd_json.relationships?.forEach((r) => {
    const rel = r.type === "one-to-many" ? "||--o{" : "||--||"
    lines.push(`    ${r.from.toUpperCase()} ${rel} ${r.to.toUpperCase()} : relates`)
  })

  // Add entities
  ;(erd_json.entities || []).forEach((entity) => {
    lines.push(`    ${entity.name.toUpperCase()} {`)
    const attrs = entity.attributes || entity.columns || []
    attrs.forEach((attr) => {
      const keyIndicator = attr.primaryKey ? " PK" : attr.foreignKey ? " FK" : ""
      lines.push(`        ${attr.type} ${attr.name}${keyIndicator}`)
    })
    lines.push("    }")
  })

  return lines.join("\n")
}

export default function ERDGenerator() {
  const [formData, setFormData] = useState<{
    model_type: string
    business_requirement: string
    erp_system_name: string
    fantasy_mode: boolean
    excel_file: File | null
  }>({
    model_type: "",
    business_requirement: "",
    erp_system_name: "",
    fantasy_mode: false,
    excel_file: null,
  })

  const [response, setResponse] = useState<APIResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [jsonCollapsed, setJsonCollapsed] = useState(true)

  // Add this after the useState declarations, before the handleInputChange function
  useEffect(() => {
    console.log("Response state changed:", response)
    if (response?.erd_json) {
      console.log("ERD JSON in state:", response.erd_json)
    }
  }, [response])

  const handleInputChange = (field: string, value: string | boolean) => {
    setFormData((prev) => ({ ...prev, [field]: value }))
    // Clear error when user starts typing
    if (error) setError(null)
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    setFormData((prev) => ({ ...prev, excel_file: file }))
    if (error) setError(null)
  }

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setLoading(true)
    setError(null)

    try {
      // Create FormData for multipart/form-data submission
      const formDataToSend = new FormData()

      // Add form fields
      formDataToSend.append("model_type", formData.model_type)
      formDataToSend.append("business_requirement", formData.business_requirement)
      formDataToSend.append("erp_system_name", formData.erp_system_name)
      formDataToSend.append("fantasy_mode", formData.fantasy_mode.toString())

      // Add file if present
      if (formData.excel_file) {
        formDataToSend.append("file", formData.excel_file)
      }

      // Make POST request to /generate-erd
      const apiResponse = await fetch("http://localhost:8000/generate-erd", {
        method: "POST",
        body: formDataToSend,
      })

      if (!apiResponse.ok) {
        const errorData = await apiResponse.json().catch(() => ({}))
        throw new Error(errorData.message || `HTTP error! status: ${apiResponse.status}`)
      }

      const responseData = await apiResponse.json()

      // Enhanced debugging
      console.log("=== API RESPONSE DEBUG ===")
      console.log("Full API Response:", responseData)
      console.log("Response type:", typeof responseData)
      console.log("Has erd_json?", !!responseData.erd_json)
      console.log("ERD JSON:", responseData.erd_json)
      console.log("ERD JSON type:", typeof responseData.erd_json)
      console.log("Entities count:", responseData.erd_json?.entities?.length)
      console.log("Summary exists?", !!responseData.summary)
      console.log("Fantasy entities count:", responseData.fantasy_entities?.length)
      console.log("=== END DEBUG ===")

      // Update state with actual response data
      console.log("Setting response state...")
      setResponse(responseData)
      console.log("Response state set successfully")
    } catch (error) {
      console.error("Error generating ERD:", error)
      const errorMessage = error instanceof Error ? error.message : "An unknown error occurred"
      setError(errorMessage)
    } finally {
      setLoading(false)
    }
  }

  const mermaidCode = response?.erd_json ? generateMermaid(response.erd_json) : ""

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 p-4">
      <div className="max-w-7xl mx-auto space-y-8">
        {/* Header */}
        <div className="text-center space-y-4">
          <div className="flex items-center justify-center gap-3">
            <Database className="w-8 h-8 text-blue-600" />
            <h1 className="text-4xl font-bold text-slate-800">ERD Schema Generator</h1>
          </div>
          <p className="text-slate-600 text-lg max-w-2xl mx-auto">
            Generate Entity Relationship Diagrams from your business requirements and data structures
          </p>
        </div>

        {/* Error Display */}
        {error && (
          <Card className="shadow-lg border-red-200">
            <CardContent className="p-6">
              <div className="flex items-center gap-3 text-red-700">
                <AlertCircle className="w-5 h-5" />
                <div>
                  <h3 className="font-semibold">Error Generating ERD</h3>
                  <p className="text-sm text-red-600">{error}</p>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Configuration Section */}
          <div className="space-y-6">
            <Card className="shadow-lg">
              <CardHeader className="bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-t-lg">
                <CardTitle className="flex items-center gap-2">
                  <FileText className="w-5 h-5" />
                  Configuration
                </CardTitle>
                <CardDescription className="text-blue-100">Configure your ERD generation parameters</CardDescription>
              </CardHeader>
              <CardContent className="p-6 space-y-6">
                <form onSubmit={handleSubmit} className="space-y-6">
                  {/* Model Type */}
                  <div className="space-y-2">
                    <Label htmlFor="model_type" className="text-sm font-medium">
                      Model Type
                    </Label>
                    <Select
                      value={formData.model_type}
                      onValueChange={(value) => handleInputChange("model_type", value)}
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Select model type" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="erp-based">ERP-based</SelectItem>
                        <SelectItem value="generic">Generic</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  {/* Business Requirements */}
                  <div className="space-y-2">
                    <Label htmlFor="business_requirement" className="text-sm font-medium">
                      Business Requirements
                    </Label>
                    <Textarea
                      id="business_requirement"
                      placeholder="Describe your business requirements and data relationships..."
                      value={formData.business_requirement}
                      onChange={(e) => handleInputChange("business_requirement", e.target.value)}
                      className="min-h-[120px] resize-none"
                    />
                  </div>

                  {/* ERP System Name */}
                  <div className="space-y-2">
                    <Label htmlFor="erp_system_name" className="text-sm font-medium">
                      ERP System Name (Optional)
                    </Label>
                    <Input
                      id="erp_system_name"
                      placeholder="e.g., SAP, Oracle, Dynamics 365"
                      value={formData.erp_system_name}
                      onChange={(e) => handleInputChange("erp_system_name", e.target.value)}
                    />
                  </div>

                  {/* Fantasy Mode Toggle */}
                  <div className="flex items-center justify-between p-4 bg-slate-50 rounded-lg">
                    <div className="space-y-1">
                      <Label htmlFor="fantasy_mode" className="text-sm font-medium flex items-center gap-2">
                        <Sparkles className="w-4 h-4 text-purple-600" />
                        Fantasy Mode
                      </Label>
                      <p className="text-xs text-slate-600">Generate additional creative entities</p>
                    </div>
                    <Switch
                      id="fantasy_mode"
                      checked={formData.fantasy_mode}
                      onCheckedChange={(checked) => handleInputChange("fantasy_mode", checked)}
                    />
                  </div>

                  {/* File Upload */}
                  <div className="space-y-2">
                    <Label htmlFor="excel_file" className="text-sm font-medium">
                      Excel File Upload
                    </Label>
                    <div className="border-2 border-dashed border-slate-300 rounded-lg p-6 text-center hover:border-slate-400 transition-colors">
                      <Upload className="w-8 h-8 text-slate-400 mx-auto mb-2" />
                      <Input
                        id="excel_file"
                        type="file"
                        accept=".xlsx,.xls"
                        onChange={handleFileChange}
                        className="hidden"
                      />
                      <Label htmlFor="excel_file" className="cursor-pointer">
                        <span className="text-sm text-slate-600">
                          {formData.excel_file ? formData.excel_file.name : "Click to upload Excel file"}
                        </span>
                        <p className="text-xs text-slate-500 mt-1">Columns: Table Name, Column Name</p>
                      </Label>
                    </div>
                  </div>

                  {/* Submit Button */}
                  <Button
                    type="submit"
                    className="w-full bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800"
                    disabled={loading}
                  >
                    {loading ? (
                      <>
                        <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                        Generating ERD...
                      </>
                    ) : (
                      "Generate ERD"
                    )}
                  </Button>
                </form>
              </CardContent>
            </Card>
          </div>

          {/* Results Section - Always Visible */}
          <div className="space-y-6">
            {/* Analysis Summary */}
            <Card className="shadow-lg">
              <CardHeader className="bg-gradient-to-r from-green-600 to-green-700 text-white rounded-t-lg">
                <CardTitle className="flex items-center gap-2">
                  <BarChart3 className="w-5 h-5" />
                  Analysis Summary
                </CardTitle>
              </CardHeader>
              <CardContent className="p-6">
                {response?.summary ? (
                  <div className="prose prose-sm max-w-none">
                    <pre className="whitespace-pre-wrap text-sm text-slate-700 font-sans leading-relaxed">
                      {response.summary}
                    </pre>
                  </div>
                ) : (
                  <div className="text-center py-12 text-slate-500">
                    <BarChart3 className="w-12 h-12 mx-auto mb-4 text-slate-300" />
                    <p className="text-lg font-medium mb-2">No Analysis Yet</p>
                    <p className="text-sm">Generate an ERD to see the analysis summary here</p>
                  </div>
                )}
              </CardContent>
            </Card>

            {/* ERD JSON Data */}
            <Card className="shadow-lg">
              <Collapsible open={!jsonCollapsed} onOpenChange={setJsonCollapsed}>
                <CollapsibleTrigger asChild>
                  <CardHeader className="bg-gradient-to-r from-purple-600 to-purple-700 text-white rounded-t-lg cursor-pointer hover:from-purple-700 hover:to-purple-800 transition-colors">
                    <CardTitle className="flex items-center justify-between">
                      <span className="flex items-center gap-2">
                        <Database className="w-5 h-5" />
                        ERD JSON Data
                      </span>
                      <ChevronDown className={`w-5 h-5 transition-transform ${!jsonCollapsed ? "rotate-180" : ""}`} />
                    </CardTitle>
                  </CardHeader>
                </CollapsibleTrigger>
                <CollapsibleContent>
                  <CardContent className="p-6">
                    {/* Debug information */}
                    <div className="mb-4 p-3 bg-yellow-50 border border-yellow-200 rounded text-xs">
                      <strong>Debug Info:</strong>
                      <div>Response exists: {response ? "✅ Yes" : "❌ No"}</div>
                      {response && (
                        <>
                          <div>Response keys: {Object.keys(response).join(", ")}</div>
                          <div>Has erd_json: {response.erd_json ? "✅ Yes" : "❌ No"}</div>
                          <div>erd_json type: {typeof response.erd_json}</div>
                          {response.erd_json && <div>Entities count: {response.erd_json.entities?.length || 0}</div>}
                        </>
                      )}
                    </div>

                    {response?.erd_json ? (
                      <pre className="bg-slate-100 p-4 rounded-lg text-xs overflow-auto max-h-96">
                        {JSON.stringify(response.erd_json, null, 2)}
                      </pre>
                    ) : response ? (
                      <div className="text-center py-8 text-orange-500">
                        <Database className="w-8 h-8 mx-auto mb-3 text-orange-300" />
                        <p className="text-sm">ERD JSON data not found in response</p>
                        <pre className="text-xs mt-2 bg-orange-50 p-2 rounded max-w-full overflow-auto">
                          {JSON.stringify(response, null, 2)}
                        </pre>
                      </div>
                    ) : (
                      <div className="text-center py-8 text-slate-500">
                        <Database className="w-8 h-8 mx-auto mb-3 text-slate-300" />
                        <p className="text-sm">JSON data will appear here after generation</p>
                      </div>
                    )}
                  </CardContent>
                </CollapsibleContent>
              </Collapsible>
            </Card>

            {/* Fantasy Entities - Only show when fantasy mode is enabled */}
            {formData.fantasy_mode && (
              <Card className="shadow-lg border-purple-200">
                <CardHeader className="bg-gradient-to-r from-purple-100 to-purple-200">
                  <CardTitle className="flex items-center gap-2 text-purple-800">
                    <Sparkles className="w-5 h-5" />
                    Fantasy Entities
                  </CardTitle>
                </CardHeader>
                <CardContent className="p-6">
                  {response?.fantasy_entities ? (
                    <div className="space-y-4">
                      {response.fantasy_entities.map((entity, index) => (
                        <div key={index} className="bg-purple-50 p-4 rounded-lg">
                          <h4 className="font-semibold text-purple-800 mb-2">{entity.name}</h4>
                          <div className="space-y-1">
                            {(entity.attributes || []).map((attr, attrIndex) => (
                              <div key={attrIndex} className="text-sm text-purple-700">
                                <span className="font-mono">{attr.name}</span>
                                <span className="text-purple-600"> ({attr.type})</span>
                                {attr.primary_key && <span className="text-purple-800 font-semibold"> PK</span>}
                              </div>
                            ))}
                          </div>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="text-center py-8 text-purple-500">
                      <Sparkles className="w-8 h-8 mx-auto mb-3 text-purple-300" />
                      <p className="text-sm">Fantasy entities will appear here after generation</p>
                    </div>
                  )}
                </CardContent>
              </Card>
            )}
          </div>
        </div>

        {/* Entity Relationship Diagram - Always Visible */}
        <Card className="shadow-lg">
          <CardHeader className="bg-gradient-to-r from-indigo-600 to-indigo-700 text-white rounded-t-lg">
            <CardTitle className="flex items-center gap-2">
              <Database className="w-5 h-5" />
              Entity Relationship Diagram
            </CardTitle>
          </CardHeader>
          <CardContent className="p-6">
            {response?.erd_json ? (
              <ERDDiagram erdData={response.erd_json} />
            ) : response ? (
              <div className="text-center py-16 text-orange-500">
                <Database className="w-16 h-16 mx-auto mb-4 text-orange-300" />
                <p className="text-xl font-medium mb-2">ERD JSON Not Found</p>
                <p className="text-sm mb-4">Check console for full response data</p>
                <pre className="text-xs bg-orange-50 p-4 rounded max-w-md mx-auto">
                  Response keys: {Object.keys(response).join(", ")}
                </pre>
              </div>
            ) : (
              <div className="text-center py-16 text-slate-500">
                <Database className="w-16 h-16 mx-auto mb-4 text-slate-300" />
                <p className="text-xl font-medium mb-2">No Diagram Generated</p>
                <p className="text-sm">Your Entity Relationship Diagram will appear here after generation</p>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
