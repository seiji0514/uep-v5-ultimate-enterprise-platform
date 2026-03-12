import { jsPDF } from 'jspdf';
import autoTable from 'jspdf-autotable';

export function downloadPdfReport(data: {
  title: string;
  generatedAt: string;
  medical?: { patients: number; ai: number; vitals: number };
  aviation?: { flights: number; airports: number };
  space?: { satellites: number; launches: number };
}) {
  const doc = new jsPDF();
  doc.setFontSize(18);
  doc.text(data.title, 14, 22);
  doc.setFontSize(10);
  doc.text(`Generated: ${data.generatedAt}`, 14, 30);

  let y = 40;
  if (data.medical) {
    doc.setFontSize(12);
    doc.text('Medical', 14, y);
    y += 8;
    autoTable(doc, {
      startY: y,
      head: [['Metric', 'Count']],
      body: [
        ['Patients', String(data.medical.patients)],
        ['AI Diagnoses', String(data.medical.ai)],
        ['Vital Records', String(data.medical.vitals)],
      ],
    });
    y = (doc as unknown as { lastAutoTable: { finalY: number } }).lastAutoTable.finalY + 15;
  }
  if (data.aviation) {
    doc.setFontSize(12);
    doc.text('Aviation', 14, y);
    y += 8;
    autoTable(doc, {
      startY: y,
      head: [['Metric', 'Count']],
      body: [
        ['Flights', String(data.aviation.flights)],
        ['Airports', String(data.aviation.airports)],
      ],
    });
    y = (doc as unknown as { lastAutoTable: { finalY: number } }).lastAutoTable.finalY + 15;
  }
  if (data.space) {
    doc.setFontSize(12);
    doc.text('Space', 14, y);
    y += 8;
    autoTable(doc, {
      startY: y,
      head: [['Metric', 'Count']],
      body: [
        ['Satellites', String(data.space.satellites)],
        ['Launches', String(data.space.launches)],
      ],
    });
  }
  doc.save('uep_report.pdf');
}
