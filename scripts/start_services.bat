@echo off
setlocal

sc start DICOMGatewayAPI
sc start DICOMGatewayReceiver
sc start DICOMGatewayWorker

endlocal
