"""
Academic Research Magic Commands

Specialized IPython magic commands for academic researchers.
"""

import os
import pandas as pd
import numpy as np
from pathlib import Path
from IPython.core.magic import Magics, magics_class, line_magic, cell_magic
from IPython.core.magic_arguments import (argument, magic_arguments, parse_argstring)
from IPython.display import display, HTML, Markdown
import matplotlib.pyplot as plt
import seaborn as sns

try:
    import sweetviz as sv
    SWEETVIZ_AVAILABLE = True
except ImportError:
    SWEETVIZ_AVAILABLE = False

from ..magic_commands import AIAssistantMagics


@magics_class
class AcademicResearchMagics(AIAssistantMagics):
    """Academic research-focused magic commands."""
    
    def __init__(self, shell=None):
        super().__init__(shell)
        self.research_context = {}
        self.current_dataset = None
        self.research_question = None
    
    @line_magic
    @magic_arguments()
    @argument('filepath', help='Path to CSV file')
    @argument('--research_question', '-q', help='Research question to guide analysis')
    @argument('--target_variable', '-t', help='Target variable for analysis')
    def research_load(self, line):
        """Load research data and perform initial analysis."""
        args = parse_argstring(self.research_load, line)
        
        try:
            # Load data
            df = pd.read_csv(args.filepath)
            self.current_dataset = df
            
            # Store research context
            if args.research_question:
                self.research_question = args.research_question
            
            # Display basic info
            display(HTML(f"""
            <div style="background: #e8f5e8; padding: 15px; border-radius: 5px; margin: 10px 0;">
                <h3>📊 Dataset Loaded Successfully</h3>
                <p><strong>File:</strong> {args.filepath}</p>
                <p><strong>Shape:</strong> {df.shape[0]} rows × {df.shape[1]} columns</p>
                {f'<p><strong>Research Question:</strong> {args.research_question}</p>' if args.research_question else ''}
            </div>
            """))
            
            # Show data preview
            display(HTML("<h4>Data Preview:</h4>"))
            display(df.head())
            
            # Show data types and missing values
            info_df = pd.DataFrame({
                'Column': df.columns,
                'Data Type': df.dtypes,
                'Missing Values': df.isnull().sum(),
                'Missing %': (df.isnull().sum() / len(df) * 100).round(2)
            })
            
            display(HTML("<h4>Data Quality Summary:</h4>"))
            display(info_df)
            
            # AI-powered initial insights
            if self.clients:
                insights_prompt = f"""
                Analyze this dataset for academic research:
                - Dataset shape: {df.shape}
                - Columns: {list(df.columns)}
                - Data types: {dict(df.dtypes)}
                - Missing values: {dict(df.isnull().sum())}
                {f'- Research question: {args.research_question}' if args.research_question else ''}
                
                Provide:
                1. Initial data quality assessment
                2. Suggested data cleaning steps
                3. Recommended analysis approaches
                4. Potential research insights to explore
                """
                
                try:
                    response = self._get_ai_response(insights_prompt, 'auto', 0.3)
                    display(Markdown(f"**🤖 AI Research Assistant Insights:**\n\n{response}"))
                except Exception as e:
                    display(HTML(f'<div style="color: orange;">AI insights unavailable: {str(e)}</div>'))
            
        except Exception as e:
            display(HTML(f'<div style="color: red;">Error loading data: {str(e)}</div>'))
    
    @line_magic
    @magic_arguments()
    @argument('--interactive', '-i', action='store_true', help='Interactive cleaning mode')
    def research_clean(self, line):
        """AI-guided data cleaning for research."""
        args = parse_argstring(self.research_clean, line)
        
        if self.current_dataset is None:
            display(HTML('<div style="color: red;">No dataset loaded. Use %research_load first.</div>'))
            return
        
        df = self.current_dataset.copy()
        
        display(HTML("<h3>🧹 AI-Guided Data Cleaning</h3>"))
        
        # Analyze data quality issues
        issues = []
        
        # Missing values
        missing_cols = df.columns[df.isnull().any()].tolist()
        if missing_cols:
            issues.append(f"Missing values in: {missing_cols}")
        
        # Potential duplicates
        duplicates = df.duplicated().sum()
        if duplicates > 0:
            issues.append(f"Potential duplicate rows: {duplicates}")
        
        # Data type issues
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        categorical_cols = df.select_dtypes(include=['object']).columns
        
        if len(issues) == 0:
            display(HTML('<div style="color: green;">✅ No major data quality issues detected!</div>'))
            return
        
        # AI recommendations
        if self.clients:
            cleaning_prompt = f"""
            As a research data analyst, recommend cleaning steps for this dataset:
            
            Data issues identified:
            {chr(10).join(f'- {issue}' for issue in issues)}
            
            Dataset context:
            - Shape: {df.shape}
            - Numeric columns: {list(numeric_cols)}
            - Categorical columns: {list(categorical_cols)}
            {f'- Research question: {self.research_question}' if self.research_question else ''}
            
            Provide specific, actionable cleaning recommendations with Python code examples.
            Consider research best practices and statistical validity.
            """
            
            try:
                response = self._get_ai_response(cleaning_prompt, 'auto', 0.2)
                display(Markdown(f"**🤖 AI Cleaning Recommendations:**\n\n{response}"))
            except Exception as e:
                display(HTML(f'<div style="color: orange;">AI recommendations unavailable: {str(e)}</div>'))
        
        # Show cleaning options
        display(HTML("""
        <div style="background: #fff3cd; padding: 15px; border-radius: 5px; margin: 10px 0;">
            <h4>🛠️ Cleaning Actions Available:</h4>
            <ul>
                <li><code>%research_clean_missing</code> - Handle missing values</li>
                <li><code>%research_clean_duplicates</code> - Remove duplicates</li>
                <li><code>%research_clean_outliers</code> - Detect and handle outliers</li>
                <li><code>%research_validate</code> - Validate cleaned data</li>
            </ul>
        </div>
        """))
    
    @line_magic
    def research_eda(self, line):
        """Generate comprehensive exploratory data analysis."""
        if self.current_dataset is None:
            display(HTML('<div style="color: red;">No dataset loaded. Use %research_load first.</div>'))
            return
        
        df = self.current_dataset
        
        display(HTML("<h3>📊 Exploratory Data Analysis</h3>"))
        
        # SweetViz report if available
        if SWEETVIZ_AVAILABLE:
            try:
                display(HTML("<h4>🍭 SweetViz Automated Report</h4>"))
                report = sv.analyze(df)
                report.show_html('research_eda_report.html', open_browser=False)
                
                display(HTML("""
                <div style="background: #d4edda; padding: 15px; border-radius: 5px; margin: 10px 0;">
                    <p>📄 <strong>SweetViz report generated:</strong> <code>research_eda_report.html</code></p>
                    <p>Open this file in your browser for interactive exploration.</p>
                </div>
                """))
                
            except Exception as e:
                display(HTML(f'<div style="color: orange;">SweetViz report failed: {str(e)}</div>'))
        else:
            display(HTML("""
            <div style="background: #fff3cd; padding: 15px; border-radius: 5px; margin: 10px 0;">
                <p>💡 <strong>Tip:</strong> Install SweetViz for automated EDA reports:</p>
                <code>pip install sweetviz</code>
            </div>
            """))
        
        # Basic statistical summary
        display(HTML("<h4>📈 Statistical Summary</h4>"))
        display(df.describe())
        
        # Correlation analysis for numeric variables
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 1:
            display(HTML("<h4>🔗 Correlation Analysis</h4>"))
            
            plt.figure(figsize=(10, 8))
            correlation_matrix = df[numeric_cols].corr()
            sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
            plt.title('Variable Correlations')
            plt.tight_layout()
            plt.show()
        
        # AI-powered insights
        if self.clients:
            eda_prompt = f"""
            Analyze this dataset for academic research insights:
            
            Dataset overview:
            - Shape: {df.shape}
            - Numeric variables: {list(numeric_cols)}
            - Categorical variables: {list(df.select_dtypes(include=['object']).columns)}
            - Statistical summary: {df.describe().to_string()}
            {f'- Research question: {self.research_question}' if self.research_question else ''}
            
            Provide:
            1. Key patterns and relationships in the data
            2. Interesting findings for research
            3. Suggested statistical tests or analyses
            4. Potential research hypotheses to test
            5. Variables that might need transformation
            """
            
            try:
                response = self._get_ai_response(eda_prompt, 'auto', 0.4)
                display(Markdown(f"**🤖 AI Research Insights:**\n\n{response}"))
            except Exception as e:
                display(HTML(f'<div style="color: orange;">AI insights unavailable: {str(e)}</div>'))
    
    @line_magic
    @magic_arguments()
    @argument('--test_type', '-t', help='Specific statistical test to perform')
    @argument('--variables', '-v', help='Variables to analyze (comma-separated)')
    def research_stats(self, line):
        """AI-guided statistical analysis."""
        args = parse_argstring(self.research_stats, line)
        
        if self.current_dataset is None:
            display(HTML('<div style="color: red;">No dataset loaded. Use %research_load first.</div>'))
            return
        
        df = self.current_dataset
        
        display(HTML("<h3>📊 Statistical Analysis</h3>"))
        
        # AI recommendations for statistical tests
        if self.clients:
            stats_prompt = f"""
            As a research statistician, recommend appropriate statistical analyses for this dataset:
            
            Dataset context:
            - Shape: {df.shape}
            - Numeric variables: {list(df.select_dtypes(include=[np.number]).columns)}
            - Categorical variables: {list(df.select_dtypes(include=['object']).columns)}
            {f'- Research question: {self.research_question}' if self.research_question else ''}
            {f'- Requested test type: {args.test_type}' if args.test_type else ''}
            {f'- Variables of interest: {args.variables}' if args.variables else ''}
            
            Provide:
            1. Recommended statistical tests with justification
            2. Assumptions to check before running tests
            3. Python code examples for the analyses
            4. How to interpret results in research context
            5. Effect size calculations where appropriate
            """
            
            try:
                response = self._get_ai_response(stats_prompt, 'auto', 0.2)
                display(Markdown(f"**🤖 Statistical Analysis Recommendations:**\n\n{response}"))
            except Exception as e:
                display(HTML(f'<div style="color: orange;">AI recommendations unavailable: {str(e)}</div>'))
        
        # Basic statistical tests based on data
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        categorical_cols = df.select_dtypes(include=['object']).columns
        
        if len(numeric_cols) >= 2:
            display(HTML("<h4>🔍 Correlation Tests</h4>"))
            from scipy.stats import pearsonr
            
            # Example correlation test
            if len(numeric_cols) >= 2:
                var1, var2 = numeric_cols[0], numeric_cols[1]
                corr, p_value = pearsonr(df[var1].dropna(), df[var2].dropna())
                
                display(HTML(f"""
                <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 10px 0;">
                    <p><strong>Correlation Test:</strong> {var1} vs {var2}</p>
                    <p><strong>Correlation coefficient:</strong> {corr:.4f}</p>
                    <p><strong>P-value:</strong> {p_value:.4f}</p>
                    <p><strong>Interpretation:</strong> {'Significant' if p_value < 0.05 else 'Not significant'} correlation</p>
                </div>
                """))
    
    @line_magic
    def research_report(self, line):
        """Generate academic research report."""
        if self.current_dataset is None:
            display(HTML('<div style="color: red;">No dataset loaded. Use %research_load first.</div>'))
            return
        
        df = self.current_dataset
        
        display(HTML("<h3>📄 Research Report Generation</h3>"))
        
        if self.clients:
            report_prompt = f"""
            Generate an academic research report section based on this data analysis:
            
            Dataset information:
            - Sample size: {df.shape[0]}
            - Variables: {df.shape[1]}
            - Variable types: {dict(df.dtypes)}
            {f'- Research question: {self.research_question}' if self.research_question else ''}
            
            Generate a "Results" section that includes:
            1. Sample description and demographics
            2. Descriptive statistics
            3. Key findings with statistical support
            4. Tables and figures references
            5. Academic writing style appropriate for publication
            
            Use proper academic language and statistical reporting standards.
            """
            
            try:
                response = self._get_ai_response(report_prompt, 'auto', 0.3)
                display(Markdown(f"**📝 Generated Research Report Section:**\n\n{response}"))
                
                # Save to file
                with open('research_report_section.md', 'w') as f:
                    f.write(response)
                
                display(HTML("""
                <div style="background: #d4edda; padding: 15px; border-radius: 5px; margin: 10px 0;">
                    <p>💾 <strong>Report saved:</strong> <code>research_report_section.md</code></p>
                </div>
                """))
                
            except Exception as e:
                display(HTML(f'<div style="color: orange;">AI report generation unavailable: {str(e)}</div>'))
    
    @line_magic
    @magic_arguments()
    @argument('query', help='Search query for research papers')
    @argument('--sources', '-s', help='Sources to search (arxiv,pubmed,core)', default='arxiv,core')
    @argument('--max_results', '-n', type=int, help='Maximum results per source', default=5)
    def research_papers(self, line):
        """Search for research papers across academic databases."""
        args = parse_argstring(self.research_papers, line)
        
        try:
            from .data_sources import search_research_papers
            
            sources = [s.strip() for s in args.sources.split(',')]
            results = search_research_papers(args.query, sources, args.max_results)
            
            display(HTML(f"<h3>📚 Research Papers for '{args.query}'</h3>"))
            
            for source, papers in results.items():
                if papers:
                    display(HTML(f"<h4>🔍 {source.upper()} Results:</h4>"))
                    
                    for i, paper in enumerate(papers, 1):
                        authors_str = ', '.join(paper.get('authors', ['Unknown']))
                        if len(authors_str) > 100:
                            authors_str = authors_str[:100] + '...'
                        
                        summary = paper.get('summary', 'No summary available')
                        if len(summary) > 200:
                            summary = summary[:200] + '...'
                        
                        display(HTML(f"""
                        <div style="background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #007bff;">
                            <h5>{i}. {paper.get('title', 'Unknown Title')}</h5>
                            <p><strong>Authors:</strong> {authors_str}</p>
                            <p><strong>Published:</strong> {paper.get('published', 'Unknown')}</p>
                            <p><strong>Summary:</strong> {summary}</p>
                            <p><strong>URL:</strong> <a href="{paper.get('url', '#')}" target="_blank">View Paper</a></p>
                        </div>
                        """))
                else:
                    display(HTML(f"<p>No results found in {source.upper()}</p>"))
            
            # AI-powered literature analysis
            if self.clients and results:
                all_papers = []
                for papers in results.values():
                    all_papers.extend(papers)
                
                if all_papers:
                    papers_summary = "\n".join([
                        f"- {paper['title']}: {paper.get('summary', '')[:100]}..."
                        for paper in all_papers[:10]
                    ])
                    
                    analysis_prompt = f"""
                    Analyze these research papers related to "{args.query}":
                    
                    {papers_summary}
                    
                    Provide:
                    1. Key themes and trends in the research
                    2. Research gaps or opportunities
                    3. Most relevant papers for further reading
                    4. Suggested research directions
                    """
                    
                    try:
                        response = self._get_ai_response(analysis_prompt, 'auto', 0.3)
                        display(Markdown(f"**🤖 AI Literature Analysis:**\n\n{response}"))
                    except Exception as e:
                        display(HTML(f'<div style="color: orange;">AI analysis unavailable: {str(e)}</div>'))
        
        except ImportError:
            display(HTML('<div style="color: red;">Research data sources not available. Install required packages.</div>'))
        except Exception as e:
            display(HTML(f'<div style="color: red;">Error searching papers: {str(e)}</div>'))
    
    @line_magic
    @magic_arguments()
    @argument('--domain', '-d', help='Research domain (education, health, social, etc.)')
    @argument('--type', '-t', help='Dataset type (survey, experimental, longitudinal)')
    def research_datasets(self, line):
        """Discover available research datasets."""
        args = parse_argstring(self.research_datasets, line)
        
        try:
            from .data_sources import get_research_datasets
            
            datasets = get_research_datasets(args.domain)
            
            display(HTML("<h3>📊 Available Research Datasets</h3>"))
            
            if datasets:
                for i, dataset in enumerate(datasets, 1):
                    display(HTML(f"""
                    <div style="background: #e8f5e8; padding: 15px; margin: 10px 0; border-radius: 5px;">
                        <h4>{i}. {dataset.get('name', dataset.get('title', 'Unknown Dataset'))}</h4>
                        <p><strong>Description:</strong> {dataset.get('description', 'No description available')}</p>
                        <p><strong>Size:</strong> {dataset.get('instances', dataset.get('size', 'Unknown'))} instances</p>
                        <p><strong>Features:</strong> {dataset.get('attributes', 'Unknown')} attributes</p>
                        <p><strong>Domain:</strong> {dataset.get('area', dataset.get('domain', 'General'))}</p>
                        {f'<p><strong>URL:</strong> <a href="{dataset["url"]}" target="_blank">Access Dataset</a></p>' if dataset.get('url') else ''}
                    </div>
                    """))
            else:
                display(HTML('<p>No datasets found for the specified criteria.</p>'))
            
            # Show how to load datasets
            display(HTML("""
            <div style="background: #fff3cd; padding: 15px; border-radius: 5px; margin: 10px 0;">
                <h4>💡 How to Load Datasets:</h4>
                <p>Use <code>%research_load_dataset dataset_name</code> to automatically load and analyze a dataset.</p>
                <p>Or upload your own CSV file with <code>%research_load your_file.csv</code></p>
            </div>
            """))
            
        except ImportError:
            display(HTML('<div style="color: red;">Research data sources not available.</div>'))
        except Exception as e:
            display(HTML(f'<div style="color: red;">Error finding datasets: {str(e)}</div>'))
    
    @line_magic
    @magic_arguments()
    @argument('indicator', help='World Bank indicator code or name')
    @argument('--country', '-c', help='Country code (default: USA)', default='USA')
    @argument('--years', '-y', help='Year range (e.g., 2010-2020)', default='2010-2020')
    def research_worldbank(self, line):
        """Access World Bank development data."""
        args = parse_argstring(self.research_worldbank, line)
        
        try:
            from .data_sources import AcademicDataSources, get_world_bank_indicators
            
            # Parse year range
            if '-' in args.years:
                start_year, end_year = map(int, args.years.split('-'))
            else:
                start_year = end_year = int(args.years)
            
            data_sources = AcademicDataSources()
            
            # Show available indicators if requested
            if args.indicator.lower() in ['list', 'help', 'indicators']:
                indicators = get_world_bank_indicators()
                display(HTML("<h3>🌍 Available World Bank Indicators</h3>"))
                
                for indicator in indicators:
                    display(HTML(f"""
                    <div style="background: #f0f8ff; padding: 10px; margin: 5px 0; border-radius: 3px;">
                        <strong>{indicator['code']}</strong>: {indicator['name']}
                    </div>
                    """))
                
                display(HTML("""
                <div style="background: #fff3cd; padding: 15px; border-radius: 5px; margin: 10px 0;">
                    <p><strong>Usage:</strong> <code>%research_worldbank NY.GDP.PCAP.CD --country USA --years 2010-2020</code></p>
                </div>
                """))
                return
            
            # Get the data
            df = data_sources.get_world_bank_data(args.indicator, args.country, start_year, end_year)
            
            if not df.empty:
                display(HTML(f"<h3>🌍 World Bank Data: {args.indicator}</h3>"))
                display(HTML(f"<p><strong>Country:</strong> {args.country} | <strong>Years:</strong> {start_year}-{end_year}</p>"))
                
                # Display the data
                display(df)
                
                # Simple visualization
                if len(df) > 1:
                    plt.figure(figsize=(10, 6))
                    plt.plot(df.index, df.iloc[:, 0])
                    plt.title(f'{args.indicator} - {args.country}')
                    plt.xlabel('Year')
                    plt.ylabel('Value')
                    plt.grid(True, alpha=0.3)
                    plt.tight_layout()
                    plt.show()
                
                # Store for further analysis
                self.current_dataset = df
                
                display(HTML("""
                <div style="background: #d4edda; padding: 15px; border-radius: 5px; margin: 10px 0;">
                    <p>✅ <strong>Data loaded successfully!</strong> You can now use other research commands to analyze this data.</p>
                    <p>Try: <code>%research_eda</code> or <code>%research_stats</code></p>
                </div>
                """))
            else:
                display(HTML('<div style="color: red;">No data found for the specified parameters.</div>'))
                
        except ImportError:
            display(HTML('<div style="color: red;">World Bank data access not available. Install wbdata package.</div>'))
        except Exception as e:
            display(HTML(f'<div style="color: red;">Error accessing World Bank data: {str(e)}</div>'))
    
    @line_magic
    def research_help(self, line):
        """Show help for academic research commands."""
        help_html = """
        <div style="font-family: monospace; background: #f5f5f5; padding: 15px; border-radius: 5px;">
        <h3>🎓 Academic Research Assistant Commands</h3>
        
        <h4>📚 Literature & Data Discovery:</h4>
        <ul>
            <li><code>%research_papers "machine learning education" --sources arxiv,pubmed</code> - Search research papers</li>
            <li><code>%research_datasets --domain education</code> - Find research datasets</li>
            <li><code>%research_worldbank NY.GDP.PCAP.CD --country USA</code> - Access World Bank data</li>
        </ul>
        
        <h4>📊 Data Loading & Exploration:</h4>
        <ul>
            <li><code>%research_load data.csv --research_question "Your question"</code> - Load and analyze dataset</li>
            <li><code>%research_eda</code> - Comprehensive exploratory data analysis</li>
            <li><code>%research_clean --interactive</code> - AI-guided data cleaning</li>
        </ul>
        
        <h4>📈 Statistical Analysis:</h4>
        <ul>
            <li><code>%research_stats --test_type "t-test"</code> - Statistical analysis recommendations</li>
            <li><code>%research_validate</code> - Validate analysis assumptions</li>
        </ul>
        
        <h4>📝 Research Output:</h4>
        <ul>
            <li><code>%research_report</code> - Generate academic report section</li>
            <li><code>%research_export --format "latex"</code> - Export results for publication</li>
        </ul>
        
        <h4>🔍 Example Research Workflow:</h4>
        <pre>
# 1. Find relevant literature
%research_papers "student engagement online learning" --sources arxiv,core

# 2. Discover datasets
%research_datasets --domain education

# 3. Load your research data
%research_load survey_data.csv --research_question "What factors predict student satisfaction?"

# 4. Explore the data
%research_eda

# 5. Clean the data with AI guidance
%research_clean --interactive

# 6. Perform statistical analysis
%research_stats --variables "satisfaction,engagement,support"

# 7. Generate research report
%research_report
        </pre>
        
        <h4>🌍 Open Data Sources Available:</h4>
        <ul>
            <li><strong>arXiv</strong> - Physics, math, computer science preprints</li>
            <li><strong>PubMed</strong> - Medical and life science literature</li>
            <li><strong>CORE</strong> - Open access research papers</li>
            <li><strong>World Bank</strong> - Development and economic indicators</li>
            <li><strong>UCI ML Repository</strong> - Machine learning datasets</li>
            <li><strong>Kaggle</strong> - Community datasets (with API setup)</li>
        </ul>
        
        <h4>🎯 Designed for Non-Technical Researchers:</h4>
        <ul>
            <li>No coding required - just magic commands</li>
            <li>AI explains statistical concepts in plain English</li>
            <li>Automated report generation in academic style</li>
            <li>Access to millions of research papers and datasets</li>
            <li>Publication-ready outputs</li>
        </ul>
        </div>
        """
        display(HTML(help_html))


def load_ipython_extension(ipython):
    """Load the academic research extension in IPython/Jupyter."""
    magics = AcademicResearchMagics(ipython)
    
    # Data loading and analysis commands
    ipython.register_magic_function(magics.research_load, 'line', 'research_load')
    ipython.register_magic_function(magics.research_clean, 'line', 'research_clean')
    ipython.register_magic_function(magics.research_eda, 'line', 'research_eda')
    ipython.register_magic_function(magics.research_stats, 'line', 'research_stats')
    ipython.register_magic_function(magics.research_report, 'line', 'research_report')
    
    # Literature and data discovery commands
    ipython.register_magic_function(magics.research_papers, 'line', 'research_papers')
    ipython.register_magic_function(magics.research_datasets, 'line', 'research_datasets')
    ipython.register_magic_function(magics.research_worldbank, 'line', 'research_worldbank')
    
    # Help command
    ipython.register_magic_function(magics.research_help, 'line', 'research_help')
    
    print("🎓 Academic Research Assistant loaded!")
    print("📚 Now with access to research papers and open datasets!")
    print("Use %research_help to see all available commands.")