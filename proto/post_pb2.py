# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: proto/post.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'proto/post.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10proto/post.proto\x12\x05proto\x1a\x1bgoogle/protobuf/empty.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"\xd1\x01\n\x04Post\x12\x0f\n\x07post_id\x18\x01 \x01(\x05\x12\r\n\x05title\x18\x02 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\x12\x12\n\ncreator_id\x18\x04 \x01(\x05\x12\x12\n\nis_private\x18\x05 \x01(\x08\x12\x0c\n\x04tags\x18\x06 \x03(\t\x12.\n\ncreated_at\x18\x07 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12.\n\nupdated_at\x18\x08 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\"2\n\x0bPostRequest\x12\x0f\n\x07post_id\x18\x01 \x01(\x05\x12\x12\n\ncreator_id\x18\x02 \x01(\x05\")\n\x0cPostResponse\x12\x19\n\x04post\x18\x01 \x01(\x0b\x32\x0b.proto.Post\"m\n\x11\x43reatePostRequest\x12\r\n\x05title\x18\x01 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\x12\x12\n\ncreator_id\x18\x03 \x01(\x05\x12\x12\n\nis_private\x18\x04 \x01(\x08\x12\x0c\n\x04tags\x18\x05 \x03(\t\"8\n\x11\x44\x65letePostRequest\x12\x0f\n\x07post_id\x18\x01 \x01(\x05\x12\x12\n\ncreator_id\x18\x02 \x01(\x05\"~\n\x11UpdatePostRequest\x12\x0f\n\x07post_id\x18\x01 \x01(\x05\x12\r\n\x05title\x18\x02 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\x12\x12\n\nis_private\x18\x04 \x01(\x08\x12\x0c\n\x04tags\x18\x05 \x03(\t\x12\x12\n\ncreator_id\x18\x06 \x01(\x05\"1\n\x10ListPostsRequest\x12\r\n\x05limit\x18\x01 \x01(\x05\x12\x0e\n\x06offset\x18\x02 \x01(\x05\"/\n\x11ListPostsResponse\x12\x1a\n\x05posts\x18\x01 \x03(\x0b\x32\x0b.proto.Post\"F\n\x0bPostComment\x12\x0f\n\x07post_id\x18\x01 \x01(\x05\x12\x15\n\rcomment_owner\x18\x03 \x01(\x05\x12\x0f\n\x07\x63omment\x18\x04 \x01(\t\"5\n\x0fPostLikeRequest\x12\x0f\n\x07post_id\x18\x01 \x01(\x05\x12\x11\n\tcaller_id\x18\x02 \x01(\x05\"7\n\x11PostUnlikeRequest\x12\x0f\n\x07post_id\x18\x01 \x01(\x05\x12\x11\n\tcaller_id\x18\x02 \x01(\x05\"I\n\x12PostCommentRequest\x12\x0f\n\x07post_id\x18\x01 \x01(\x05\x12\x11\n\tcaller_id\x18\x02 \x01(\x05\x12\x0f\n\x07\x63ontent\x18\x03 \x01(\t\"5\n\x0fPostViewRequest\x12\x0f\n\x07post_id\x18\x01 \x01(\x05\x12\x11\n\tcaller_id\x18\x03 \x01(\x05\"*\n\x17PostCommentsListRequest\x12\x0f\n\x07post_id\x18\x01 \x01(\x05\"@\n\x18PostCommentsListResponse\x12$\n\x08\x63omments\x18\x01 \x03(\x0b\x32\x12.proto.PostComment2\x8e\x05\n\x0cPostsService\x12;\n\nCreatePost\x12\x18.proto.CreatePostRequest\x1a\x13.proto.PostResponse\x12>\n\nDeletePost\x12\x18.proto.DeletePostRequest\x1a\x16.google.protobuf.Empty\x12>\n\nUpdatePost\x12\x18.proto.UpdatePostRequest\x1a\x16.google.protobuf.Empty\x12\x32\n\x07GetPost\x12\x12.proto.PostRequest\x1a\x13.proto.PostResponse\x12>\n\tListPosts\x12\x17.proto.ListPostsRequest\x1a\x18.proto.ListPostsResponse\x12:\n\x08LikePost\x12\x16.proto.PostLikeRequest\x1a\x16.google.protobuf.Empty\x12>\n\nUnLikePost\x12\x18.proto.PostUnlikeRequest\x1a\x16.google.protobuf.Empty\x12@\n\x0b\x43ommentPost\x12\x19.proto.PostCommentRequest\x1a\x16.google.protobuf.Empty\x12:\n\x08ViewPost\x12\x16.proto.PostViewRequest\x1a\x16.google.protobuf.Empty\x12S\n\x10ListCommentsPost\x12\x1e.proto.PostCommentsListRequest\x1a\x1f.proto.PostCommentsListResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'proto.post_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_POST']._serialized_start=90
  _globals['_POST']._serialized_end=299
  _globals['_POSTREQUEST']._serialized_start=301
  _globals['_POSTREQUEST']._serialized_end=351
  _globals['_POSTRESPONSE']._serialized_start=353
  _globals['_POSTRESPONSE']._serialized_end=394
  _globals['_CREATEPOSTREQUEST']._serialized_start=396
  _globals['_CREATEPOSTREQUEST']._serialized_end=505
  _globals['_DELETEPOSTREQUEST']._serialized_start=507
  _globals['_DELETEPOSTREQUEST']._serialized_end=563
  _globals['_UPDATEPOSTREQUEST']._serialized_start=565
  _globals['_UPDATEPOSTREQUEST']._serialized_end=691
  _globals['_LISTPOSTSREQUEST']._serialized_start=693
  _globals['_LISTPOSTSREQUEST']._serialized_end=742
  _globals['_LISTPOSTSRESPONSE']._serialized_start=744
  _globals['_LISTPOSTSRESPONSE']._serialized_end=791
  _globals['_POSTCOMMENT']._serialized_start=793
  _globals['_POSTCOMMENT']._serialized_end=863
  _globals['_POSTLIKEREQUEST']._serialized_start=865
  _globals['_POSTLIKEREQUEST']._serialized_end=918
  _globals['_POSTUNLIKEREQUEST']._serialized_start=920
  _globals['_POSTUNLIKEREQUEST']._serialized_end=975
  _globals['_POSTCOMMENTREQUEST']._serialized_start=977
  _globals['_POSTCOMMENTREQUEST']._serialized_end=1050
  _globals['_POSTVIEWREQUEST']._serialized_start=1052
  _globals['_POSTVIEWREQUEST']._serialized_end=1105
  _globals['_POSTCOMMENTSLISTREQUEST']._serialized_start=1107
  _globals['_POSTCOMMENTSLISTREQUEST']._serialized_end=1149
  _globals['_POSTCOMMENTSLISTRESPONSE']._serialized_start=1151
  _globals['_POSTCOMMENTSLISTRESPONSE']._serialized_end=1215
  _globals['_POSTSSERVICE']._serialized_start=1218
  _globals['_POSTSSERVICE']._serialized_end=1872
# @@protoc_insertion_point(module_scope)
