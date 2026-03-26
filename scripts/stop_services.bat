@echo off
setlocal

sc stop DICOMGatewayAPI
sc stop DICOMGatewayReceiver
sc stop DICOMGatewayWorker

endlocal
