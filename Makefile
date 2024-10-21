.PHONY: package clean deploy_local

# Variables
PACKAGE_DIR = package
SOURCE_DIR = src/python
ZIP_DIR = src/terraform/archive
TF_DIR = src/terraform
ZIPFILE = $(ZIP_DIR)/image-uploader.zip

# Package command to install dependencies and create the zip file
package: clean
	mkdir -p $(PACKAGE_DIR) && \
	mkdir -p $(ZIP_DIR) && \
	pip install -r requirements.txt --target $(PACKAGE_DIR) && \
	cp -r $(SOURCE_DIR)/* $(PACKAGE_DIR)
	cd $(PACKAGE_DIR) && \
	zip -r9u ../${ZIPFILE} ./*

deploy_local: package
	cd $(TF_DIR) && \
	tflocal apply --auto-approve
	make clean

# Clean up generated files
clean:
	rm -rf $(PACKAGE_DIR)