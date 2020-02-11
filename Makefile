ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

.PHONY: protobuf

protobuf:
	find ${ROOT_DIR}/protobuf/*.proto -exec \
		protoc \
			-I="${ROOT_DIR}/protobuf/" \
			--python_out="${ROOT_DIR}/python/include/ubiquity/serialization" \
			{} \;