# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: model.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0bmodel.proto\"x\n\x0b\x43leanedData\x12\x0f\n\x07x_train\x18\x01 \x03(\x01\x12\x0f\n\x07y_train\x18\x02 \x03(\x01\x12\x0e\n\x06x_test\x18\x03 \x03(\x01\x12\x0e\n\x06y_test\x18\x04 \x03(\x01\x12\x13\n\x0b\x64\x61tes_train\x18\x05 \x03(\t\x12\x12\n\ndates_test\x18\x06 \x03(\t\"\x89\x01\n\rTrainResponse\x12\r\n\x05model\x18\x01 \x01(\x0c\x12\x0f\n\x07x_train\x18\x02 \x03(\x01\x12\x0f\n\x07y_train\x18\x03 \x03(\x01\x12\x0e\n\x06x_test\x18\x04 \x03(\x01\x12\x0e\n\x06y_test\x18\x05 \x03(\x01\x12\x13\n\x0b\x64\x61tes_train\x18\x06 \x03(\t\x12\x12\n\ndates_test\x18\x07 \x03(\t2=\n\x0fTrainingService\x12*\n\nTrainModel\x12\x0c.CleanedData\x1a\x0e.TrainResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'model_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_CLEANEDDATA']._serialized_start=15
  _globals['_CLEANEDDATA']._serialized_end=135
  _globals['_TRAINRESPONSE']._serialized_start=138
  _globals['_TRAINRESPONSE']._serialized_end=275
  _globals['_TRAININGSERVICE']._serialized_start=277
  _globals['_TRAININGSERVICE']._serialized_end=338
# @@protoc_insertion_point(module_scope)
