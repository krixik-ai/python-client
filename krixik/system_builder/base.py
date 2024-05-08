import time
import copy
import os
import tempfile
from typing import Optional
from krixik.__version__ import __version__
from krixik.utilities.validators.system import EXPIRE_TIME_DEFAULT
from krixik.system_builder.functions.checkin import checkin
from krixik.system_builder.functions.list_files import list_files
from krixik.system_builder.functions.fetch_output import fetch_output
from krixik.system_builder.functions.show_tree import show_post
from krixik.system_builder.functions.show_tree import show_illustration
from krixik.system_builder.functions.update import update
from krixik.system_builder.functions.process import process_local_file
from krixik.system_builder.functions.process import get_presigned_url
from krixik.system_builder.functions.delete import delete_server_files
from krixik.system_builder.functions.check_process_status import check_process_status
from krixik.system_builder.functions.check_process_status import process_status_reporter
from krixik.utilities.utilities import vprint
from krixik.utilities.file_name_generator import generate_random_file_name
from krixik.system_builder.functions.checkin import check_init_decorator
from krixik.utilities.converters.utilities.decorators import datatype_converter_wrapper
from krixik.utilities.validators.utilities.decorators import type_check_inputs
from krixik.modules.utilities.decorators import type_check_inputs as type_check_modules
from krixik.system_builder.utilities.decorators import kwargs_checker


class KrixikBasePipeline:
    def __init__(
        self,
        *,
        pipeline: str | None = None,
        module_chain: list,
        output_process_keys: list,
        api_key: Optional[str] = None,
        api_url: Optional[str] = None,
        api_check_val: Optional[int] = None,
    ) -> None:
        # inherit necessary custom pipeline variables
        self.__pipeline = pipeline
        self.__pipeline_ordered_modules = module_chain
        self.__pipeline_output_process_keys = output_process_keys
        self.__first_module = self.__pipeline_ordered_modules[0]
        self.__last_module = self.__pipeline_ordered_modules[-1]

        self.__version = __version__
        self.__api_key = api_key
        self.__api_url = api_url
        self.__api_check_val = api_check_val
        self.converted_file_path = None
        self.cleaned_file_path = None
        self.file_id = None
        self.request_id = None
        self.process_id = None
        self.upload_results = None
        self.wait_for_process = False
        self.file_name = None
        self.symbolic_directory_path = None
        self.file_tags = None
        self.file_description = None
        self.modules = None
        self.local_file_path = None
        self.__local_conversion_directory = tempfile.gettempdir()

    @property
    def module_chain(self):
        return self.__pipeline_ordered_modules

    @property
    def pipeline_output_process_keys(self):
        return self.__pipeline_output_process_keys

    @property
    def first_module(self):
        return self.__first_module

    @property
    def last_module(self):
        return self.__last_module

    @property
    def local_conversion_directory(self):
        return self.__local_conversion_directory

    @property
    def api_key(self):
        return self.__api_key

    @property
    def api_url(self):
        return self.__api_url

    @property
    def api_check_val(self):
        return self.__api_check_val

    @property
    def version(self):
        return self.__version

    @property
    def pipeline(self):
        return self.__pipeline

    @pipeline.setter
    def pipeline_name(self, value):
        self.__pipeline = value

    @type_check_inputs
    def init(self, *, api_key: str | None, api_url: str | None) -> None:
        """initialize pipeline with an api_key and api_url

        Parameters
        ----------
        api_key : str | None
            valid api_key, by default None
        api_url : str | None
            valid api_url, by default None
        """
        self.__api_key = api_key
        self.__api_url = api_url
        self.__api_check_val = checkin(self.__api_key, self.__api_url)

    @check_init_decorator
    def __delete_server_files(self) -> dict:
        return delete_server_files(self)

    @kwargs_checker
    @check_init_decorator
    @type_check_inputs
    def delete(self, *, file_id: str = None) -> dict:
        """delete a file from the server via its file_id for a given pipeline

        Parameters
        ----------
        file_id : str
            the file_id of the file to be deleted, by default None

        Returns
        -------
        dict
            a dictionary containing the status_code, request_id, and message indicating success or failure
        """
        if file_id is None:
            raise ValueError("please provide a file_id")
        self.file_id = file_id
        return self.__delete_server_files()

    @kwargs_checker
    @check_init_decorator
    @type_check_inputs
    def list(
        self,
        *,
        file_ids: list | None = None,
        file_names: list | None = None,
        symbolic_directory_paths: list | None = None,
        symbolic_file_paths: list | None = None,
        file_tags: list | None = None,
        sort_order: str = "descending",
        max_files: int | None = None,
        created_at_start: str | None = None,
        created_at_end: str | None = None,
        last_updated_start: str | None = None,
        last_updated_end: str | None = None,
        verbose: bool = False,
    ) -> dict:
        """list files on the server for a given pipeline

        Parameters
        ----------
        file_ids : list | None, optional
            list of file_ids to filter by, by default None
        file_names : list | None, optional
            list of file_names to filter by, by default None
        symbolic_directory_paths : list | None, optional
            list of symbolic_directory_paths to filter by, by default None
        symbolic_file_paths : list | None, optional
            list of symbolic_file_paths to filter by, by default None
        file_tags : list | None, optional
            list of file_tags to filter by, by default None
        sort_order : str, optional
            the sort order of the results, by default "descending"
        max_files : int | None, optional
            the maximum number of files to return, by default None
        created_at_start : str | None, optional
            start date for created_at filter, by default None
        created_at_end : str | None, optional
            end date for created_at filter, by default None
        last_updated_start : str | None, optional
            start date for last_updated filter, by default None
        last_updated_end : str | None, optional
            end date for last_updated filter, by default None
        verbose : bool, optional
            whether to print verbose output, by default True

        Returns
        -------
        dict
            a dictionary containing the status_code, request_id, any return items, and message indicating success or failure
        """
        if sort_order == "global":
            raise ValueError("sort order must be either 'descending' or 'ascending'")
        return list_files(
            self,
            file_ids=file_ids,
            file_names=file_names,
            symbolic_directory_paths=symbolic_directory_paths,
            symbolic_file_paths=symbolic_file_paths,
            file_tags=file_tags,
            sort_order=sort_order,
            max_files=max_files,
            created_at_start=created_at_start,
            created_at_end=created_at_end,
            last_updated_start=last_updated_start,
            last_updated_end=last_updated_end,
            verbose=verbose,
        )

    @kwargs_checker
    @check_init_decorator
    @type_check_inputs
    def fetch_output(self, *, file_id: str, local_save_directory: str = os.getcwd()) -> dict | None:
        """fetch the output of a file from the server via its file_id for a given pipeline

        Parameters
        ----------
        file_id : str
            the file_id of the file to be fetched, by default None
        local_save_directory: str, optional
            the local save directory to store process output, default is current working directory

        Returns
        -------
        dict | None
            a dictionary containing the status_code, request_id, and message indicating success or failure
        """
        return fetch_output(self, file_id, local_save_directory)

    @kwargs_checker
    @check_init_decorator
    @type_check_inputs
    def update(
        self,
        *,
        file_id: str = None,
        file_name: Optional[str] = None,
        symbolic_directory_path: Optional[str] = None,
        symbolic_file_path: Optional[str] = None,
        file_tags: Optional[dict] = None,
        file_description: Optional[str] = None,
        expire_time: Optional[str] = None,
        verbose: bool = True,
    ) -> dict:
        """update the metadata of a file def show_on the server via its file_id for a given pipeline

        Parameters
        ----------
        file_id : str, optional
            the file_id of the file to be updated, by default None
        file_name : str, optional
            the new file_name of the file, by default None
        symbolic_directory_path : str, optional
            the new symbolic_directory_path of the file, by default None
        symbolic_file_path : str, optional
            the new symbolic_file_path of the file, by default None
        file_tags : dict, optional
            the new file_tags of the file, by default None
        file_description : str, optional
            the new file_description of the file, by default None
        expire_time : str, optional
            the new expire_time of the file, by default None
        verbose : bool, optional
            whether to print verbose output, by default True

        Returns
        -------
        dict
            a dictionary containing the status_code, request_id, and message indicating success or failure
        """
        return update(
            self,
            file_id=file_id,
            file_name=file_name,
            symbolic_directory_path=symbolic_directory_path,
            symbolic_file_path=symbolic_file_path,
            file_tags=file_tags,
            file_description=file_description,
            expire_time=expire_time,
            verbose=verbose,
        )

    def _get_presigned_url(self, payload_data: dict) -> tuple[bool, dict]:
        return get_presigned_url(self, payload_data)

    def _reset_class_variables(self) -> None:
        self.file_name = None
        self.symbolic_directory_path = None
        self.file_tags = None
        self.file_description = None
        self.modules = None
        self.local_file_path = None
        self.__presigned_post_url_results = None
        self.file_id = None
        self.request_id = None
        self.process_id = None
        self.upload_results = None

    def __upload_file_to_s3_via_presignedurl(self, verbose: bool = True) -> None:
        # process local file to s3 via presigned url
        upload_status_repeater_success, upload_response = process_local_file(self)

        try:
            if upload_response.status_code == 204:
                if not self.wait_for_process:
                    vprint("INFO: wait_for_process is set to False.", verbose=verbose)
                    vprint(
                        "INFO: File upload complete, processing has now started on our servers.  ide control will now be returned to you.",
                        verbose=verbose,
                    )
                    vprint(
                        "INFO: You will be able to check the status of this file's processing using the .process_status api as shown below.",
                        verbose=verbose,
                    )
                    vprint(
                        f"INFO: This process's request_id is: {self.process_id}.",
                        verbose=verbose,
                    )
                    vprint(
                        f"INFO: Check the status of this file's processing: .process_status(request_id='{self.process_id}').",
                        verbose=verbose,
                    )
                    return

                if self.wait_for_process:
                    vprint("INFO: File process and processing status:", verbose=verbose)
                    # check process status every timestep seconds for maximum of 600 seconds
                    timestep = 3
                    max_count = 200

                    # check process status for the first time
                    file_id, process_status, failure_status, message = check_process_status(self, process_id=self.process_id)

                    if failure_status is not None:
                        self.__delete_server_files()
                        if "failure_module" in list(failure_status.keys()):
                            raise ValueError(
                                f"processes associated with file_id {file_id} and request_id {self.process_id} failed at module {failure_status['failure_module']}"
                            )
                        else:
                            raise ValueError(f"processes associated with file_id {file_id} and request_id {self.process_id} failed")

                    prev_process_status = None
                    process_status_reporter(self, prev_process_status, process_status, verbose=verbose)
                    process_complete = False
                    process_count = 0
                    while not process_complete and process_count < max_count - 1:
                        # create process_status memory dict
                        prev_process_status = copy.deepcopy(process_status)

                        # check status
                        file_id, process_status, failure_status, message = check_process_status(self, process_id=self.process_id)

                        if failure_status is not None:
                            self.__delete_server_files()
                            if "failure_module" in list(failure_status.keys()):
                                raise ValueError(
                                    f"processes associated with request_id '{failure_status['process_id']}' failed at module '{failure_status['failure_module']}'"
                                )
                            else:
                                raise ValueError(f"processes associated with request_id '{failure_status['process_id']}' failed")

                        # report status
                        process_complete = process_status_reporter(self, prev_process_status, process_status, verbose=verbose)

                        process_count += 1
                        time.sleep(timestep)

                    if not process_complete or process_count == max_count - 1:
                        exception_message = f"file process status check timed out - the request_id of this failed process is {self.process_id}."
                        self.__delete_server_files()

                        raise ValueError(exception_message)
                    vprint("SUCCESS: pipeline process complete.", verbose=verbose)
            else:
                exception_message = f"pipeline process failed with status code: {upload_response.status_code} - the request_id of this failed process is {self.process_id}"
                self.__delete_server_files()

                raise ValueError(exception_message)
        except ValueError as err:
            raise err

    @kwargs_checker
    @check_init_decorator
    @datatype_converter_wrapper
    @type_check_modules
    @type_check_inputs
    def process(
        self,
        *,
        file_name: Optional[str] = None,
        symbolic_directory_path: Optional[str] = None,
        symbolic_file_path: Optional[str] = None,
        local_file_path: Optional[str] = None,
        file_tags: Optional[list] = None,
        file_description: Optional[str] = None,
        modules: Optional[dict] = {},
        expire_time: Optional[int] = None,
        verbose: bool = True,
        wait_for_process: bool = True,
        local_save_directory: str = os.getcwd(),
        og_local_file_path: Optional[str] = None,
    ) -> dict | None:
        """process a file to the server for a given pipeline

        Parameters
        ----------
        file_name : str, optional
            the name of the file, by default None
        symbolic_directory_path : str, optional
            the symbolic directory path of the file, by default None
        symbolic_file_path : str, optional
            the symbolic file path of the file, by default None
        local_file_path : str, optional
            the local file path of the file, by default None
        file_tags : list, optional
            the tags of the file, by default None
        file_description : str, optional
            the description of the file, by default None
        local_save_directory : str, optional
            the local save directory of the file, by default None
        modules : dict, optional
            the modules selected to process associated input file, by default None
        expire_time : int, optional
            the expire time of the file, by default None
        verbose : bool, optional
            whether to print verbose output, by default True
        wait_for_process : bool, optional
            whether to process the file asynchronously, by default False
        local_save_directory: str
            local directory for process output, by default os.getcwd()
        og_local_file_path: str, optional
            local file path used for any file conversion (e.g., mp4 to mp3, controlled internally
        Returns
        -------
        dict | None
            a dictionary containing the status_code, request_id, and message indicating success or failure
        """

        if local_file_path is None:
            raise ValueError("local_file_path cannot be empty")

        if (file_name is not None or symbolic_directory_path is not None) and symbolic_file_path is not None:
            raise ValueError("file_name and symbolic_directory_path cannot both be given if symbolic_file_path is given")

        if symbolic_directory_path is None:
            symbolic_directory_path = "/etc"
            vprint(
                "INFO: symbolic_directory_path was not set by user - setting to default of /etc",
                verbose=verbose,
            )

        if file_name is None:
            file_name = generate_random_file_name(local_file_path.split(".")[-1])
            vprint(
                f"INFO: file_name was not set by user - setting to random file name: {file_name}",
                verbose=verbose,
            )

        if expire_time is None:
            vprint(
                f"INFO: expire_time was not set by user - setting to default of {EXPIRE_TIME_DEFAULT} seconds",
                verbose=verbose,
            )
            expire_time = EXPIRE_TIME_DEFAULT

        vprint(f"INFO: wait_for_process is set to {wait_for_process}.", verbose=verbose)

        # report date of expire_time based on current_time and expire_time
        current_time = time.time()
        expire_time_date = str(time.ctime(current_time + int(expire_time))).strip()
        vprint(
            f"INFO: file will expire and be removed from you account in {expire_time} seconds, at {expire_time_date} UTC",
            verbose=verbose,
        )

        self.local_file_path = local_file_path
        self.modules = modules
        self.wait_for_process = wait_for_process
        self.file_name = file_name
        self.symbolic_directory_path = symbolic_directory_path
        self.file_tags = file_tags
        self.file_description = file_description

        payload_data = {
            "pipeline": self.__pipeline,
            "pipeline_ordered_modules": self.__pipeline_ordered_modules,
            "pipeline_output_process_keys": self.__pipeline_output_process_keys,
            "modules": self.modules,
            "version": self.__version,
            "file_name": self.file_name,
            "symbolic_directory_path": (self.symbolic_directory_path if self.symbolic_directory_path is not None else "/etc"),
            "file_tags": self.file_tags if self.file_tags is not None else [],
            "file_description": (self.file_description if self.file_description is not None else ""),
            "expire_time": expire_time,
        }

        # get presigned url and file_id
        upload_check, self.upload_results = self._get_presigned_url(payload_data=payload_data)

        if not upload_check:
            # return failure signal
            raise ValueError(self.upload_results["message"])

        vprint(
            f"INFO: {self.__pipeline} file process and input processing started...",
            verbose=verbose,
        )
        if "warnings" in self.upload_results:
            for warning in self.upload_results["warnings"]:
                vprint(warning, verbose=verbose)
            vprint("INFO: metadata can be updated using the .update api.", verbose=verbose)

        # unpack upload_results
        self.__presigned_post_url_results = self.upload_results["presigned_post_url_results"]

        self.file_id = self.upload_results["file_id"]
        self.process_id = self.upload_results["request_id"]
        vprint(
            f"INFO: This process's request_id is: {self.process_id}",
            verbose=verbose,
        )

        # package output data
        output_data = {
            "file_id": self.file_id,
            "request_id": self.process_id,
            "file_name": self.file_name,
            "symbolic_directory_path": self.symbolic_directory_path,
            "file_tags": self.file_tags,
            "file_description": self.file_description,
        }

        # process s3 file via presigned url
        self.__upload_file_to_s3_via_presignedurl(verbose=verbose)

        # reset class variables
        self._reset_class_variables()

        if not self.wait_for_process:
            return output_data

        if output_data is not None:
            try:
                file_id = output_data["file_id"]
                file_output = self.fetch_output(file_id=file_id, local_save_directory=local_save_directory)
                vprint("SUCCESS: process output downloaded", verbose=verbose)
                return file_output
            except Exception as e:
                raise e

        return output_data

    @kwargs_checker
    @check_init_decorator
    @type_check_inputs
    def show_tree(
        self,
        *,
        symbolic_directory_path: str = "/*",
        max_files: int = 1000,
        verbose: bool = True,
    ) -> dict | None:
        """show the tree of files on the server for a given pipeline

        Parameters
        ----------
        symbolic_directory_path : str,
            symbolic_directory_path or stump to visualize, by default /*
        max_files : int
            the maximum number of files to return, by default 1000
        verbose : bool
            whether to print verbose output, by default False

        Returns
        -------
        dict | None
            a dictionary containing the status_code, request_id, and message indicating success or failure
        """

        # make request
        results = show_post(self, symbolic_directory_path=symbolic_directory_path, max_files=max_files, verbose=verbose)

        # show illustration
        show_illustration(self, results=results)

        return_object = {
            "status_code": results["status_code"],
            "items": results["items"],
            "request_id": results["request_id"],
            "message": results["message"],
            "warnings": results["warnings"],
        }

        self._reset_class_variables()
        return return_object

    @kwargs_checker
    @check_init_decorator
    @type_check_inputs
    def process_status(self, request_id: str = None) -> dict:
        """check the status of a file processing for a given pipeline

        Parameters
        ----------
        request_id : str
            the request_id of the process to be checked, by default None

        Returns
        -------
        dict | None
            a string or dictionary containing the status_code, request_id, and message indicating success or failure
        """

        if request_id is None:
            raise TypeError("process request_id cannot be empty")

        # check status
        file_id, process_status, failure_status, message = check_process_status(self, process_id=request_id)

        report = {}
        report["status_code"] = 200
        report["request_id"] = self.request_id
        report["file_id"] = file_id
        report["message"] = message
        report["pipeline"] = self.__pipeline

        if process_status is not None:
            report["process_status"] = process_status
            report["overall_status"] = "complete"
            cleaned_process_status = {}
            keys = list(process_status.keys())
            for key in keys:
                cleaned_process_status[key.split(".")[0]] = process_status[key]
                if process_status[key] is not True:
                    report["overall_status"] = "ongoing"
            report["process_status"] = cleaned_process_status
            return report
        if failure_status is not None:
            report["failure_status"] = failure_status
            report["overall_status"] = "failed"
            return report
        return report
