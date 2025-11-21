"""
Insight Assistant for AI-powered data analysis in Jupyter notebooks.
"""

import pandas as pd
from IPython.display import display, HTML

class InsightAssistant:
    """
    AI-powered assistant to generate insights and visualizations from DataFrames.
    """

    def __init__(self):
        # This is a placeholder for the AIAssistantMagics class.
        # The actual instance will be injected from the magic command.
        self.magics = None

    def get_insights(self, df: pd.DataFrame, model: str = 'auto'):
        """
        Generate insights and visualization suggestions for a DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame to analyze.
            model (str): The AI model to use.

        Returns:
            dict: A dictionary containing 'summary' and 'visualizations'.
        """
        if not isinstance(df, pd.DataFrame):
            raise TypeError("Input must be a pandas DataFrame.")

        # Get DataFrame summary
        df_head = df.head().to_string()
        df_info = df.info(verbose=False, buf=None)

        # Create a detailed prompt for the AI
        prompt = f"""
Analyze the following pandas DataFrame and provide:
1. A brief, insightful summary of the data.
2. Three distinct and relevant visualization suggestions using Plotly Express.
   - For each suggestion, provide the Python code to generate the plot.
   - The code should be ready to execute.
   - Choose plots that are genuinely insightful for this data.
   - Do not use `fig.show()`, just the `px.` call.

DataFrame Head:
{df_head}

DataFrame Info:
{df_info}

Please format the output as a JSON object with two keys: 'summary' and 'visualizations'.
'visualizations' should be a list of strings, where each string is a single line of Plotly Express code.
"""

        try:
            response_text = self.magics._get_ai_response(prompt, model)

            # Clean up the response to extract the JSON part
            json_response = self._extract_json(response_text)

            return json_response

        except Exception as e:
            return {
                'summary': f"Error generating insights: {e}",
                'visualizations': []
            }

    def _extract_json(self, text: str) -> dict:
        """Extract JSON object from a string, handling markdown code blocks."""
        try:
            # Find the start and end of the JSON object
            start_index = text.find('{')
            end_index = text.rfind('}') + 1

            if start_index == -1 or end_index == 0:
                raise ValueError("No JSON object found in the response.")

            json_str = text[start_index:end_index]

            import json
            return json.loads(json_str)

        except (ValueError, json.JSONDecodeError) as e:
            # Fallback for simple cases if JSON parsing fails
            return {
                'summary': "Could not parse AI response.",
                'visualizations': []
            }
