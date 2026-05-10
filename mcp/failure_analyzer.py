from mcp.mcp_client import MCPClient


class FailureAnalyzer:

    def __init__(self):
        self.llm = MCPClient()

    def analyze_failure(self, test_name, error_logs):

        prompt = f"""
                    You are a QA automation expert.

                    Analyze this test failure:

                    Test Name:
                    {test_name}

                    Error Logs:
                    {error_logs}

                    Provide analysis in this format:

                    1. Root Cause
                    2. Likely Fix
                    3. Is it:
                    - Locator Issue
                    - API Issue
                    - Environment Issue
                    - Test Logic Issue

                    Be precise and practical.
                    """

        return self.llm.ask_llm(prompt)