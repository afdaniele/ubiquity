DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))/../
ROOT_DIR:=$(realpath ${DIR})

.PHONY: protobuf

protobuf:
	find ${ROOT_DIR}/ubiquity/serialization/*.proto -exec \
		protoc \
			-I="${ROOT_DIR}" \
			--python_out="${ROOT_DIR}/ubiquity/python/include" \
			{} \;
