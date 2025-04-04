# coding: utf-8

# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
FILE: sample_classify_document_async.py

DESCRIPTION:
    This sample demonstrates how to classify a document using a trained document classifier.
    To learn how to build your custom classifier, see sample_build_classifier.py.

    More details on building a classifier and labeling your data can be found here:
    https://aka.ms/azsdk/documentintelligence/buildclassifiermodel

USAGE:
    python sample_classify_document_async.py

    Set the environment variables with your own values before running the sample:
    1) DOCUMENTINTELLIGENCE_ENDPOINT - the endpoint to your Document Intelligence resource.
    2) DOCUMENTINTELLIGENCE_API_KEY - your Document Intelligence API key.
    3) CLASSIFIER_ID - the ID of your trained document classifier
        -OR-
       DOCUMENTINTELLIGENCE_TRAINING_DATA_CLASSIFIER_SAS_URL - The shared access signature (SAS) Url of your Azure Blob Storage container
       with your training files. A document classifier will be built and used to run the sample.
"""

import asyncio
import os


async def classify_document(classifier_id):
    path_to_sample_documents = os.path.abspath(
        os.path.join(
            os.path.abspath(__file__),
            "..",
            "..",
            "./sample_forms/forms/IRS-1040.pdf",
        )
    )

    from azure.core.credentials import AzureKeyCredential
    from azure.ai.documentintelligence.aio import DocumentIntelligenceClient
    from azure.ai.documentintelligence.models import AnalyzeResult

    endpoint = os.environ["DOCUMENTINTELLIGENCE_ENDPOINT"]
    key = os.environ["DOCUMENTINTELLIGENCE_API_KEY"]
    classifier_id = os.getenv("CLASSIFIER_ID", classifier_id)

    document_intelligence_client = DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    async with document_intelligence_client:
        with open(path_to_sample_documents, "rb") as f:
            poller = await document_intelligence_client.begin_classify_document(classifier_id, body=f)
        result: AnalyzeResult = await poller.result()

    print("----Classified documents----")
    if result.documents:
        for doc in result.documents:
            if doc.bounding_regions:
                print(
                    f"Found document of type '{doc.doc_type or 'N/A'}' with a confidence of {doc.confidence} contained on "
                    f"the following pages: {[region.page_number for region in doc.bounding_regions]}"
                )


async def main():
    classifier_id = None
    if os.getenv("DOCUMENTINTELLIGENCE_TRAINING_DATA_CLASSIFIER_SAS_URL") and not os.getenv("CUSTOM_BUILT_MODEL_ID"):
        import uuid
        from azure.core.credentials import AzureKeyCredential
        from azure.ai.documentintelligence.aio import DocumentIntelligenceAdministrationClient
        from azure.ai.documentintelligence.models import (
            AzureBlobContentSource,
            ClassifierDocumentTypeDetails,
            BuildDocumentClassifierRequest,
        )

        endpoint = os.environ["DOCUMENTINTELLIGENCE_ENDPOINT"]
        key = os.environ["DOCUMENTINTELLIGENCE_API_KEY"]
        blob_container_sas_url = os.environ["DOCUMENTINTELLIGENCE_TRAINING_DATA_CLASSIFIER_SAS_URL"]

        document_intelligence_admin_client = DocumentIntelligenceAdministrationClient(
            endpoint=endpoint, credential=AzureKeyCredential(key)
        )
        async with document_intelligence_admin_client:
            poller = await document_intelligence_admin_client.begin_build_classifier(
                BuildDocumentClassifierRequest(
                    classifier_id=str(uuid.uuid4()),
                    doc_types={
                        "IRS-1040-A": ClassifierDocumentTypeDetails(
                            azure_blob_source=AzureBlobContentSource(
                                container_url=blob_container_sas_url, prefix="IRS-1040-A/train"
                            )
                        ),
                        "IRS-1040-B": ClassifierDocumentTypeDetails(
                            azure_blob_source=AzureBlobContentSource(
                                container_url=blob_container_sas_url, prefix="IRS-1040-B/train"
                            )
                        ),
                    },
                )
            )
            classifier = await poller.result()
        classifier_id = classifier.classifier_id
    await classify_document(classifier_id)


if __name__ == "__main__":
    from azure.core.exceptions import HttpResponseError
    from dotenv import find_dotenv, load_dotenv

    try:
        load_dotenv(find_dotenv())
        asyncio.run(main())
    except HttpResponseError as error:
        # Examples of how to check an HttpResponseError
        # Check by error code:
        if error.error is not None:
            if error.error.code == "InvalidImage":
                print(f"Received an invalid image error: {error.error}")
            if error.error.code == "InvalidRequest":
                print(f"Received an invalid request error: {error.error}")
            # Raise the error again after printing it
            raise
        # If the inner error is None and then it is possible to check the message to get more information:
        if "Invalid request".casefold() in error.message.casefold():
            print(f"Uh-oh! Seems there was an invalid request: {error}")
        # Raise the error again
        raise
