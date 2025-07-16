"""
response = client.models.generate_content(
    model=MODEL_ID, prompt='Why is the sky blue?'
)
FileAPI to parse pdfs
file_ref = client.files.upload(file='../assets/cv-latex/alex_smith.pdf')
file_ref
"""

from .utils import get_config


class Prompter:
    def __init__(self, client, model_id="gemini-2.5-flash"):
        self.client = client
        self.model_id = model_id
        self.model = self.client.models.get
        self.config = get_config()
        self.__chat_idx = 0
        self.__history = {}

    def generate_content(self, prompt, files=[]):
        """Generate content using the specified model."""

        if files:
            file_refs = self.upload_files(files)
            prompt = (
                prompt
                + "\n"
                + "\n".join(
                    f"File reference {i} for {files[i]}: {file_ref}"
                    for i, file_ref in enumerate(file_refs)
                )
            )
        """ 
        #! only supported in Vertex AI
        tokens_used = self.client.models.count_tokens(
            model=self.model_id, contents=prompt, config=self.config
        )
        if tokens_used > 4096:
            raise ValueError(
                f"Prompt exceeds token limit: {tokens_used} tokens used, limit is 4096."
            )
        """

        response = self.client.models.generate_content(
            model=self.model_id,
            contents=prompt,
            config=self.config,
        )

        if not response:
            raise ValueError("No response received from the model.")

        self.log(prompt, response)
        return response

    def upload_files(self, files):
        """Upload files to the model."""
        file_refs = []
        for file in files:
            file_ref = self.client.files.upload(file=file)
            if not file_ref:
                raise ValueError(f"Failed to upload file: {file}")
            file_refs.append(file_ref)
        return file_refs

    def log(self, prompt, response):
        """Log the prompt and response."""

        print(f"Total tokens used: {response.usage_metadata.total_token_count}")

        self.get_finish_reason(response)

        self.__history[self.__chat_idx] = {
            "prompt": prompt,
            "response": response,
        }
        self.__chat_idx += 1

    def get_finish_reason(self, response):
        """Get the finish reason from the response."""
        finish_reason = response.candidates[0].finish_reason.strip()
        if finish_reason == "MAX_TOKENS":
            print("Warning: Response truncated due to max tokens limit.")
        else:
            print(f"Response generated successfully: {finish_reason}.")

    def get_history(self):
        """Return the conversation history."""
        return self.__history

    def reset_history(self):
        """Reset the conversation history."""
        self.__history = {}
        self.__chat_idx = 0
