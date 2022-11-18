from PyPDF2 import PdfFileWriter,PdfFileReader
import pikepdf
import pdfcrowd
import shutil
import sys
import os
# import os
# from pdfrw import PdfReader, PdfWriter, PageMerge


def decrypt(pdf_file, id):
    pdf = pikepdf.open(pdf_file)
    output = f'{id}/temp2.pdf'
    pdf.save(output)
    return output


def downloadPdf(name, id):

    print('zipping')
    if os.path.exists(f'{id}\{id}.zip'):
        os.remove(f'{id}\{id}.zip')
    shutil.make_archive(f'{id}', 'zip', f'{id}')
    print('ziped')
    try:
        # create the API client instance
        client = pdfcrowd.HtmlToPdfClient('demo', 'ce544b6ea52a5621fb9d55f8b542d14d')

        # configure the conversion
        client.setZipMainFilename('index2.html')
        # client.setCssPageRuleMode('mode1'
        client.setPageWidth('33.08in')
        client.setPageHeight('46.8in')
        client.setMarginTop('35.1in')
        client.setMarginRight('0')
        client.setMarginBottom('0')
        client.setMarginLeft('0')
        client.setConverterVersion('18.10')
        client.setDataEncoding('utf-8')
        client.setUseHttp(True)

        # run the conversion and write the result to a file
        client.convertFileToFile(f'{id}.zip', f'{id}_{name}.pdf')
        print('downloaded')
        decrypt(f'{id}_{name}.pdf', id)
        print('decrypted')
        os.remove(f'{id}.zip')


    except pdfcrowd.Error as why:
        # report the error
        sys.stderr.write('Pdfcrowd Error: {}\n'.format(why))

        # rethrow or handle the exception
        raise


def cropPdf(pdf_file, count, id):

    pdfFile = PdfFileReader(open(pdf_file, 'rb'))
    pdf_write = PdfFileWriter()

    for i in range(pdfFile.getNumPages()):
        #background = PdfFileReader(open(r'backgrounds/5.pdf', 'rb')).getPage(0)
        page = pdfFile.getPage(i)
        # print(i)
        # print(page.cropBox.getUpperRight())
        page.mediaBox.lowerRight = (613, 0)
        page.mediaBox.lowerLeft = (0, 0)
        page.mediaBox.upperRight = (613, 842)
        page.mediaBox.upperLeft = (0, 842)
        pdf_write.addPage(page)

    with open(f'{id}_{count}.pdf', 'wb') as file:
        pdf_write.write(file)
    if count == 1:
        print('creating cover pdf')
        inputpdf = PdfFileReader(open(f'{id}_{count}.pdf', "rb"))
        output = PdfFileWriter()
        output.addPage(inputpdf.getPage(0))
        with open(f'{id}/cover.pdf', "wb") as outputStream:
            output.write(outputStream)
    return f'{id}_{count}.pdf'


def dividePdf(id):
    size = os.path.getsize(f'{id}/chat.pdf')/1024/1024
    inputpdf = PdfFileReader(open(f'{id}/chat.pdf', "rb"))
    inputpdf2 = PdfFileReader(open(f'{id}/cover.pdf', "rb"))
    #inputpdf2 = PdfFileReader(open(f'front.pdf', "rb"))
    chunks = int(inputpdf.numPages/(size//20))
    pages = list(range(inputpdf.numPages))
    divided_page = [pages[i:i + chunks] for i in range(0, len(pages), chunks)]
    names = []
    x=0
    for i in divided_page:
        x = x+1
        output = PdfFileWriter()
        if not x == 1:
            output.addPage(inputpdf2.getPage(0))
        for j in i:
            output.addPage(inputpdf.getPage(j))
        name = f'{id}/chat{x}.pdf'
        names.append(name)
        with open(name, "wb") as outputStream:
            output.write(outputStream)
    os.remove(f'{id}/chat.pdf')
    return names



