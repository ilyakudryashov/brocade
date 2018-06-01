import win32com.client
import sys

appVisio = win32com.client.Dispatch("Visio.Application")
appVisio.Visible =1
doc = appVisio.Documents.Add("Basic Diagram.vst")
page = doc.Pages.Item(1)
stancils = appVisio.Documents("SAN_Health_Visio_Stencils_External.vss")
switch = stancils.Masters("GENERICSWITCH")
host = stancils.Masters("FCHOST")

def visio_connect_objects(begin,end):
    connectorMaster = appVisio.Application.ConnectorToolDataObject
    connector = page.Drop(connectorMaster, 2, 2)
    #connector.Cells("BeginArrow").FormulaU = 10
    connector.Cells("BeginX").GlueTo(begin.Cells("Connections.X1"))
    connector.Cells("EndX").GlueTo(end.Cells("Connections.X1"))

def visio_create_object(type,name,x,y):
    obj = page.Drop(type,x,y)
    obj.Text = name
    return obj

switch1 = visio_create_object(switch,'коммутатор 1', 3, 3)
switch2 = visio_create_object(switch,'коммутатор 2', 5, 3)
host1 = visio_create_object(host, 'хост 1', 4,4)

visio_connect_objects(switch1,host1)
visio_connect_objects(switch1,switch2)





#connectorMaster = appVisio.Application.ConnectorToolDataObject

#connector = page.Drop(connectorMaster, 0, 0)
#connector.Cells("BeginX").GlueTo(switch1.Cells("PinX"))
#connector.Cells("EndX").GlueTo(switch2.Cells("PinX"))

#switch1 = page.Drop(switch, 5, 2)
#switch1.Text = "switch1"

#doc.SaveAs(r'C:\Users\ia.kudryashov\PycharmProjects\brocade\MyDrawing1.vsd')
#doc.Close()

#appVisio.Visible =0
#appVisio.Quit()
