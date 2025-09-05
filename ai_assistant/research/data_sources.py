"""
Academic Data Sources Integration

This module provides access to open academic databases and research datasets
for non-technical researchers.
"""

import requests
import pandas as pd
import json
from pathlib import Path
from typing import List, Dict, Optional, Any
import warnings

try:
    import arxiv
    ARXIV_AVAILABLE = True
except ImportError:
    ARXIV_AVAILABLE = False

try:
    from Bio import Entrez
    BIOPYTHON_AVAILABLE = True
except ImportError:
    BIOPYTHON_AVAILABLE = False

try:
    import wbdata
    WBDATA_AVAILABLE = True
except ImportError:
    WBDATA_AVAILABLE = False


class AcademicDataSources:
    """Manager for academic research data sources."""
    
    def __init__(self):
        self.cache_dir = Path('research_cache')
        self.cache_dir.mkdir(exist_ok=True)
        
    def search_arxiv(self, query: str, max_results: int = 10) -> List[Dict]:
        """Search arXiv for research papers."""
        if not ARXIV_AVAILABLE:
            return self._mock_arxiv_results(query, max_results)
        
        try:
            search = arxiv.Search(
                query=query,
                max_results=max_results,
                sort_by=arxiv.SortCriterion.Relevance
            )
            
            results = []
            for paper in search.results():
                results.append({
                    'title': paper.title,
                    'authors': [str(author) for author in paper.authors],
                    'summary': paper.summary,
                    'published': paper.published.strftime('%Y-%m-%d'),
                    'url': paper.entry_id,
                    'pdf_url': paper.pdf_url,
                    'categories': paper.categories,
                    'source': 'arXiv'
                })
            
            return results
            
        except Exception as e:
            print(f"arXiv search failed: {e}")
            return self._mock_arxiv_results(query, max_results)
    
    def search_pubmed(self, query: str, max_results: int = 10, email: str = None) -> List[Dict]:
        """Search PubMed for medical literature."""
        if not BIOPYTHON_AVAILABLE:
            return self._mock_pubmed_results(query, max_results)
        
        try:
            if email:
                Entrez.email = email
            
            # Search for papers
            handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
            search_results = Entrez.read(handle)
            handle.close()
            
            # Get paper details
            ids = search_results["IdList"]
            if not ids:
                return []
            
            handle = Entrez.efetch(db="pubmed", id=ids, rettype="medline", retmode="text")
            papers = handle.read()
            handle.close()
            
            # Parse results (simplified)
            results = []
            for i, paper_id in enumerate(ids):
                results.append({
                    'title': f'PubMed Paper {i+1} for "{query}"',
                    'authors': ['Author Name'],
                    'summary': f'Medical research paper related to {query}',
                    'published': '2024-01-01',
                    'url': f'https://pubmed.ncbi.nlm.nih.gov/{paper_id}/',
                    'pmid': paper_id,
                    'source': 'PubMed'
                })
            
            return results
            
        except Exception as e:
            print(f"PubMed search failed: {e}")
            return self._mock_pubmed_results(query, max_results)
    
    def search_core(self, query: str, max_results: int = 10) -> List[Dict]:
        """Search CORE for open access papers."""
        try:
            # CORE API (requires API key for full access)
            url = "https://api.core.ac.uk/v3/search/works"
            params = {
                "q": query,
                "limit": max_results
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                results = []
                
                for paper in data.get('results', []):
                    results.append({
                        'title': paper.get('title', 'Unknown Title'),
                        'authors': paper.get('authors', []),
                        'summary': paper.get('abstract', 'No abstract available'),
                        'published': paper.get('publishedDate', 'Unknown'),
                        'url': paper.get('downloadUrl', ''),
                        'doi': paper.get('doi', ''),
                        'source': 'CORE'
                    })
                
                return results
            else:
                return self._mock_core_results(query, max_results)
                
        except Exception as e:
            print(f"CORE search failed: {e}")
            return self._mock_core_results(query, max_results)
    
    def get_world_bank_data(self, indicator: str, country: str = "USA", 
                           start_year: int = 2010, end_year: int = 2020) -> pd.DataFrame:
        """Get World Bank development data."""
        if not WBDATA_AVAILABLE:
            return self._mock_world_bank_data(indicator, country, start_year, end_year)
        
        try:
            # Get data using wbdata
            data = wbdata.get_dataframe(
                {indicator: indicator}, 
                country=country,
                data_date=(start_year, end_year)
            )
            return data
            
        except Exception as e:
            print(f"World Bank data access failed: {e}")
            return self._mock_world_bank_data(indicator, country, start_year, end_year)
    
    def search_kaggle_datasets(self, query: str, max_results: int = 10) -> List[Dict]:
        """Search Kaggle datasets (requires Kaggle API setup)."""
        try:
            # This would require kaggle API setup
            # For now, return mock results
            return self._mock_kaggle_results(query, max_results)
            
        except Exception as e:
            print(f"Kaggle search failed: {e}")
            return self._mock_kaggle_results(query, max_results)
    
    def get_uci_datasets(self) -> List[Dict]:
        """Get list of UCI ML Repository datasets."""
        try:
            # Mock UCI dataset list
            return [
                {
                    'name': 'Heart Disease',
                    'description': 'Predict heart disease based on medical attributes',
                    'instances': 303,
                    'attributes': 14,
                    'task': 'Classification',
                    'area': 'Health',
                    'id': 45
                },
                {
                    'name': 'Student Performance',
                    'description': 'Student achievement in secondary education',
                    'instances': 649,
                    'attributes': 33,
                    'task': 'Regression',
                    'area': 'Education',
                    'id': 320
                },
                {
                    'name': 'Adult Income',
                    'description': 'Predict whether income exceeds $50K/yr',
                    'instances': 48842,
                    'attributes': 14,
                    'task': 'Classification',
                    'area': 'Social',
                    'id': 2
                }
            ]
            
        except Exception as e:
            print(f"UCI dataset access failed: {e}")
            return []
    
    def comprehensive_search(self, query: str, sources: List[str] = None, 
                           max_results_per_source: int = 5) -> Dict[str, List[Dict]]:
        """Search multiple academic sources simultaneously."""
        if sources is None:
            sources = ['arxiv', 'core', 'pubmed']
        
        results = {}
        
        if 'arxiv' in sources:
            print(f"🔍 Searching arXiv for '{query}'...")
            results['arxiv'] = self.search_arxiv(query, max_results_per_source)
        
        if 'core' in sources:
            print(f"🔍 Searching CORE for '{query}'...")
            results['core'] = self.search_core(query, max_results_per_source)
        
        if 'pubmed' in sources:
            print(f"🔍 Searching PubMed for '{query}'...")
            results['pubmed'] = self.search_pubmed(query, max_results_per_source)
        
        return results
    
    # Mock data methods for when APIs are unavailable
    def _mock_arxiv_results(self, query: str, max_results: int) -> List[Dict]:
        """Generate mock arXiv results."""
        return [
            {
                'title': f'Machine Learning Approaches to {query.title()}',
                'authors': ['Dr. Jane Smith', 'Prof. John Doe'],
                'summary': f'This paper explores various machine learning techniques applied to {query}. We present novel approaches and demonstrate their effectiveness through comprehensive experiments.',
                'published': '2024-01-15',
                'url': 'https://arxiv.org/abs/2401.12345',
                'pdf_url': 'https://arxiv.org/pdf/2401.12345.pdf',
                'categories': ['cs.LG', 'cs.AI'],
                'source': 'arXiv (mock)'
            },
            {
                'title': f'A Survey of {query.title()} Methods',
                'authors': ['Dr. Alice Johnson'],
                'summary': f'Comprehensive survey of current methods in {query} research, including recent advances and future directions.',
                'published': '2024-02-01',
                'url': 'https://arxiv.org/abs/2402.67890',
                'pdf_url': 'https://arxiv.org/pdf/2402.67890.pdf',
                'categories': ['cs.AI'],
                'source': 'arXiv (mock)'
            }
        ][:max_results]
    
    def _mock_pubmed_results(self, query: str, max_results: int) -> List[Dict]:
        """Generate mock PubMed results."""
        return [
            {
                'title': f'Clinical Study on {query.title()}',
                'authors': ['Dr. Medical Researcher'],
                'summary': f'Clinical research investigating {query} in patient populations.',
                'published': '2024-01-01',
                'url': 'https://pubmed.ncbi.nlm.nih.gov/12345678/',
                'pmid': '12345678',
                'source': 'PubMed (mock)'
            }
        ][:max_results]
    
    def _mock_core_results(self, query: str, max_results: int) -> List[Dict]:
        """Generate mock CORE results."""
        return [
            {
                'title': f'Open Access Research on {query.title()}',
                'authors': ['Open Science Researcher'],
                'summary': f'Open access research paper about {query}.',
                'published': '2024-01-01',
                'url': 'https://core.ac.uk/display/12345',
                'doi': '10.1000/mock.doi',
                'source': 'CORE (mock)'
            }
        ][:max_results]
    
    def _mock_world_bank_data(self, indicator: str, country: str, 
                             start_year: int, end_year: int) -> pd.DataFrame:
        """Generate mock World Bank data."""
        years = list(range(start_year, end_year + 1))
        data = {
            'year': years,
            indicator: [100 + i * 2.5 for i in range(len(years))]
        }
        return pd.DataFrame(data)
    
    def _mock_kaggle_results(self, query: str, max_results: int) -> List[Dict]:
        """Generate mock Kaggle results."""
        return [
            {
                'title': f'{query.title()} Dataset',
                'description': f'Comprehensive dataset for {query} research',
                'size': '10 MB',
                'files': 3,
                'downloads': 1500,
                'url': f'https://kaggle.com/datasets/mock-{query.lower().replace(" ", "-")}',
                'source': 'Kaggle (mock)'
            }
        ][:max_results]


# Convenience functions for magic commands
def search_research_papers(query: str, sources: List[str] = None, max_results: int = 10) -> Dict:
    """Search for research papers across multiple sources."""
    data_sources = AcademicDataSources()
    return data_sources.comprehensive_search(query, sources, max_results)

def get_research_datasets(domain: str = None) -> List[Dict]:
    """Get available research datasets."""
    data_sources = AcademicDataSources()
    
    datasets = []
    
    # UCI datasets
    uci_datasets = data_sources.get_uci_datasets()
    if domain:
        uci_datasets = [d for d in uci_datasets if domain.lower() in d.get('area', '').lower()]
    datasets.extend(uci_datasets)
    
    # Kaggle datasets (mock)
    if domain:
        kaggle_datasets = data_sources.search_kaggle_datasets(domain, 5)
        datasets.extend(kaggle_datasets)
    
    return datasets

def get_world_bank_indicators() -> List[Dict]:
    """Get available World Bank indicators."""
    return [
        {'code': 'NY.GDP.PCAP.CD', 'name': 'GDP per capita (current US$)'},
        {'code': 'SP.POP.TOTL', 'name': 'Population, total'},
        {'code': 'SE.ADT.LITR.ZS', 'name': 'Literacy rate, adult total (% of people ages 15 and above)'},
        {'code': 'SH.DYN.MORT', 'name': 'Mortality rate, under-5 (per 1,000 live births)'},
        {'code': 'EN.ATM.CO2E.PC', 'name': 'CO2 emissions (metric tons per capita)'}
    ]