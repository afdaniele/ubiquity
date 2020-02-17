DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
ROOT_DIR:=$(realpath ${DIR}/../)

.PHONY: protobuf

protobuf:
	# Python
	find ${ROOT_DIR}/ubiquity/serialization/*.proto -exec \
		protoc \
			-I="${ROOT_DIR}" \
			--python_out="${ROOT_DIR}/ubiquity/python/include" \
			{} \;

	# Javascript (NodeJS)
	find ${ROOT_DIR}/ubiquity/serialization/*.proto -exec \
		protoc \
			-I="${ROOT_DIR}" \
			--js_out=import_style=commonjs,binary:${ROOT_DIR}/ubiquity/javascript/include/ubiquity/serialization/nodejs \
			{} \;
	npm install \
		--prefix ${ROOT_DIR}/ubiquity/javascript/include/ubiquity/serialization/nodejs/ubiquity/serialization/ \
		google-protobuf
	npm install \
		--prefix ${ROOT_DIR}/ubiquity/javascript/include/ubiquity/serialization/nodejs/ubiquity/tunnel/ \
		ws
	npm install \
		--prefix ${ROOT_DIR}/ubiquity/javascript/include/ubiquity/serialization/nodejs/ubiquity/ \
		uuid4

	# Javascript (Browser)
	mkdir -p ${ROOT_DIR}/ubiquity/serialization/js_wspace
	find ${ROOT_DIR}/ubiquity/serialization/*.proto -exec \
		protoc \
			-I="${ROOT_DIR}" \
			--js_out=import_style=commonjs,binary:${ROOT_DIR}/ubiquity/serialization/js_wspace \
			{} \;
	docker build \
		-t ubiquity:browserify \
		-f ${ROOT_DIR}/ubiquity/javascript/Dockerfile.browserify \
		${ROOT_DIR}/ubiquity/serialization/js_wspace
	docker run \
		-it --rm \
		-v ${ROOT_DIR}/ubiquity/serialization/js_wspace:/js_in \
		-v ${ROOT_DIR}/ubiquity/javascript/include/ubiquity/serialization/browser:/js_out \
		ubiquity:browserify
	rm -r ${ROOT_DIR}/ubiquity/serialization/js_wspace

