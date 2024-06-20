function downloadPDF() {
    const doc = new jsPDF();
    const element = document.querySelector('.drive-details');

    // Use html2canvas to render the HTML element as an image
    html2canvas(element).then(canvas => {
        const imageData = canvas.toDataURL('image/jpeg');

        // Add the image to the PDF
        doc.addImage(imageData, 'JPEG', 15, 15, 180, 0);

        // Download the PDF
        doc.save('drive_details.pdf');
    });
}