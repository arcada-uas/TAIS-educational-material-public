# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: data.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\ndata.proto\x12\x04\x64\x61ta\"\"\n\x0b\x44\x61taRequest\x12\x13\n\x0b\x63sv_content\x18\x01 \x01(\x0c\"y\n\x0c\x44\x61taResponse\x12\x0f\n\x07x_train\x18\x01 \x03(\x01\x12\x0e\n\x06x_test\x18\x02 \x03(\x01\x12\x0f\n\x07y_train\x18\x03 \x03(\x01\x12\x0e\n\x06y_test\x18\x04 \x03(\x01\x12\x13\n\x0b\x64\x61tes_train\x18\x05 \x03(\t\x12\x12\n\ndates_test\x18\x06 \x03(\t2A\n\x0b\x44\x61taService\x12\x32\n\tCleanData\x12\x11.data.DataRequest\x1a\x12.data.DataResponseb\x06proto3')



_DATAREQUEST = DESCRIPTOR.message_types_by_name['DataRequest']
_DATARESPONSE = DESCRIPTOR.message_types_by_name['DataResponse']
DataRequest = _reflection.GeneratedProtocolMessageType('DataRequest', (_message.Message,), {
  'DESCRIPTOR' : _DATAREQUEST,
  '__module__' : 'data_pb2'
  # @@protoc_insertion_point(class_scope:data.DataRequest)
  })
_sym_db.RegisterMessage(DataRequest)

DataResponse = _reflection.GeneratedProtocolMessageType('DataResponse', (_message.Message,), {
  'DESCRIPTOR' : _DATARESPONSE,
  '__module__' : 'data_pb2'
  # @@protoc_insertion_point(class_scope:data.DataResponse)
  })
_sym_db.RegisterMessage(DataResponse)

_DATASERVICE = DESCRIPTOR.services_by_name['DataService']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _DATAREQUEST._serialized_start=20
  _DATAREQUEST._serialized_end=54
  _DATARESPONSE._serialized_start=56
  _DATARESPONSE._serialized_end=177
  _DATASERVICE._serialized_start=179
  _DATASERVICE._serialized_end=244
# @@protoc_insertion_point(module_scope)
