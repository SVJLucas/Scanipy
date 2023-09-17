import requests
import os
import tarfile

def identify_main_tex_file(tar_ref):
    main_tex_file = None

    for file_info in tar_ref:
        if file_info.name.endswith(".tex"):
            # Read the content of the TeX file
            with tar_ref.extractfile(file_info) as tex_file:
                tex_content = tex_file.read().decode("utf-8")

            # Check if the TeX file contains criteria indicating it's the main file
            if is_main_tex_file(tex_content):
                main_tex_file = file_info
                break

    # If no main TeX file is found, fall back to the first TeX file encountered
    if main_tex_file is None and len(tar_ref.getnames()) > 0:
        main_tex_file = tar_ref.getnames()[0]

    return main_tex_file

def is_main_tex_file(tex_content):
    # Implement your logic here to determine if the TeX file is the main file
    # You can check for specific content, keywords, or patterns in the TeX file
    # For example, you might look for \begin{document} or other markers.

    # Replace this example logic with your own criteria
    return "\\begin{document}" in tex_content

def downloading_tar_pdf(df):
    # Iterate through the DataFrame and download PDFs
    for index, row in df.iterrows():
        link = row['Link']

        # Split the link by '/'
        parts = link.split('/')

        # Get the last part of the URL
        arxiv_id = parts[-1]

        # Define the directory where you want to save the files
        save_directory = "arxiv_files"
        save_tar = os.path.join(save_directory, "tars", arxiv_id)
        save_pdf = os.path.join(save_directory, "pdf")

        # Download the TeX file in a tar archive
        tex_tar_url = f"https://arxiv.org/e-print/{arxiv_id}"
        tex_tar_response = requests.get(tex_tar_url)

        # Check if the response is a tar archive
        if tex_tar_response.headers.get('content-type') == 'application/x-eprint-tar':
            # Save the tar file
            # Create the directory if it doesn't exist
            if not os.path.exists(save_tar):
                os.makedirs(save_tar)
            tar_file_path = os.path.join(save_tar, f"{arxiv_id}.tar")
            with open(tar_file_path, 'wb') as tar_file:
                tar_file.write(tex_tar_response.content)

            # Extract tar only if there is a TeX file
            tex_file_found = False
            with tarfile.open(tar_file_path, 'r') as tar_ref:
                main_tex_file = identify_main_tex_file(tar_ref)

                for file_info in tar_ref:
                    if not tex_file_found:
                        if file_info == main_tex_file:
                            tex_file_found = True

                        # Extract the file
                        tar_ref.extract(file_info, save_tar)
                        # Get the extracted file's name
                        extracted_file_name = file_info.name

                        if tex_file_found and extracted_file_name.endswith(".tex"):
                            # Rename the main TeX file to {arxiv_id}.tex
                            new_tex_file_name = f"{arxiv_id}.tex"
                            os.rename(os.path.join(save_tar, extracted_file_name),
                                      os.path.join(save_tar, new_tex_file_name))
                            #print(f"Main TeX file saved as {new_tex_file_name}")
                        else:
                            # Keep the names of auxiliary TeX files
                            os.rename(os.path.join(save_tar, extracted_file_name),
                                      os.path.join(save_tar, extracted_file_name))
                            #print(f"Auxiliary TeX file saved as {extracted_file_name}")

            # Remove the tar file after extraction
            os.remove(tar_file_path)
            #print(f"TAR files saved to {tar_file_path}")

            # If a TeX file was found, download the PDF
            if tex_file_found:
                pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
                # Create the directory if it doesn't exist
                if not os.path.exists(save_pdf):
                    os.makedirs(save_pdf)
                pdf_file_path = os.path.join(save_pdf, f"{arxiv_id}.pdf")
                pdf_response = requests.get(pdf_url)
                with open(pdf_file_path, 'wb') as pdf_file:
                    pdf_file.write(pdf_response.content)
                #print(f"PDF file saved to {pdf_file_path}")
        else:
            a=1
            ##print(f"TeX file tar archive not found for ArXiv ID: {arxiv_id}")
