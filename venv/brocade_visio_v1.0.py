import win32com.client
import sys


appVisio = win32com.client.Dispatch("Visio.Application")
appVisio.Visible =1

doc = appVisio.Documents.Add("Basic Diagram.vst")
pagObj = doc.Pages.Item(1)
stnObj = appVisio.Documents("SAN_Health_Visio_Stencils_External.vss")
mastObj = stnObj.Masters("GENERICSWITCH")

shpObj1 = pagObj.Drop(mastObj, 4.25, 5.5)
shpObj1.Text = "This is some text."

shpObj2 = pagObj.Drop(mastObj, 2, 2)
shpObj2.Text = "This is some more text."

connectorMaster = appVisio.Application.ConnectorToolDataObject

connector = pagObj.Drop(connectorMaster, 0, 0)
connector.Cells("BeginX").GlueTo(shpObj1.Cells("PinX"))
connector.Cells("EndX").GlueTo(shpObj2.Cells("PinX"))

doc.SaveAs(r'C:\Users\ia.kudryashov\PycharmProjects\brocade\MyDrawing.vsd')
doc.Close()

appVisio.Visible =0
appVisio.Quit()

#visio = win32com.client.Dispatch("Visio.Application")
#doc = visio.Documnts.Open("C:\\Users\\ia.kudryashov\\PycharmProjects\\brocade\\test.vsdx")
"""
visio = win32com.client.Dispatch("Visio.Application")
doc = visio.Documnts.Open("C:\\Users\\ia.kudryashov\\PycharmProjects\\brocade\\test.vsdx")
vsoShape1 = doc.ActivePage.DrawRectangle(1,1,2,2)
vsoShape1.Cells("LineColor").FormulaU = 0
vsoShape1.Cells("LineWeight").FormulaU = "2.0 pt"
vsoShape1.FillStyle = "None"
vsoShape1.Text = "This is a test"
vsoShape1.Cells("Char.size").FormulaU = "20 pt

appVisio = win32com.client.Dispatch("visio.application")
docsObj = appVisio.Documents
#Create a document based on the Basic Diagram template that automatically
#opens the Basic Shapes stencil.
docObj = docsObj.Add("Basic Diagram.vst")
pagsObj = appVisio.ActiveDocument.Pages
#A new document always has at least one page, whose index in the Pages collection is 1.
pagObj = pagsObj.Item(1)
stnObj = appVisio.Documents("Basic Shapes.vss")
mastObj = stnObj.Masters("Rectangle")
#Drop the rectangle in the approximate middle of the page.
#Coordinates passed with the Drop method are always inches.
shpObj = pagObj.Drop(mastObj, 4.25, 5.5)
#Set the text of the rectangle
shpObj.Text = "Hello World!"
#Save the drawing and quit Visio. The message pauses the program
#so you can see the Visio drawing before the instance closes.
#docObj.SaveAs "hello.vsd"
#MsgBox "Drawing finished!",, "Hello World!"
appVisio.Quit
"""