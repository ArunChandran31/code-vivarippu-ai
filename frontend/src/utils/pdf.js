// src/utils/pdf.js
import jsPDF from 'jspdf'

export function downloadReportPDF(title='Report', code='', ai={}, staticAnalysis={}, meta={}){
  const doc = new jsPDF()
  doc.setFontSize(14)
  doc.text(title, 10, 10)
  doc.setFontSize(10)
  doc.text('Code:', 10, 20)
  doc.setFont('courier')
  doc.text(code.slice(0,2000), 10, 28) // keep it short; can add pages
  doc.setFont('helvetica')
  doc.text('AI Summary:', 10, 120)
  doc.text(JSON.stringify(ai,null,2).slice(0,3000), 10, 128)
  doc.save(`${title.replace(/\s+/g,'_')}.pdf`)
}
