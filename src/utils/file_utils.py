"""
File handling utilities for the GenerativeAI Starter Kit
"""
import os
import json
import csv
from typing import List, Dict, Any, Optional, Union
from pathlib import Path
import hashlib
import shutil


class FileHandler:
    """File operations and document processing utilities"""
    
    def __init__(self):
        self.supported_text_formats = {'.txt', '.md', '.json', '.csv', '.py', '.js', '.html', '.xml'}
        self.supported_image_formats = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp', '.tiff'}
        self.supported_audio_formats = {'.mp3', '.wav', '.m4a', '.ogg', '.flac'}
    
    def read_text_file(self, file_path: Union[str, Path], encoding: str = 'utf-8') -> str:
        """
        Read text content from file
        
        Args:
            file_path: Path to the file
            encoding: File encoding
            
        Returns:
            File content as string
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            # Try with different encoding
            try:
                with open(file_path, 'r', encoding='latin-1') as f:
                    return f.read()
            except Exception as e:
                raise ValueError(f"Could not read file {file_path}: {e}")
    
    def write_text_file(self, file_path: Union[str, Path], content: str, encoding: str = 'utf-8') -> bool:
        """
        Write text content to file
        
        Args:
            file_path: Path to the file
            content: Content to write
            encoding: File encoding
            
        Returns:
            True if successful
        """
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(file_path, 'w', encoding=encoding) as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Error writing file {file_path}: {e}")
            return False
    
    def read_json_file(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Read JSON file
        
        Args:
            file_path: Path to JSON file
            
        Returns:
            Parsed JSON data
        """
        content = self.read_text_file(file_path)
        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in file {file_path}: {e}")
    
    def write_json_file(self, file_path: Union[str, Path], data: Dict[str, Any], indent: int = 2) -> bool:
        """
        Write data to JSON file
        
        Args:
            file_path: Path to JSON file
            data: Data to write
            indent: JSON indentation
            
        Returns:
            True if successful
        """
        try:
            json_content = json.dumps(data, indent=indent, ensure_ascii=False)
            return self.write_text_file(file_path, json_content)
        except Exception as e:
            print(f"Error writing JSON file {file_path}: {e}")
            return False
    
    def read_csv_file(self, file_path: Union[str, Path], delimiter: str = ',') -> List[Dict[str, str]]:
        """
        Read CSV file as list of dictionaries
        
        Args:
            file_path: Path to CSV file
            delimiter: CSV delimiter
            
        Returns:
            List of row dictionaries
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8', newline='') as f:
                reader = csv.DictReader(f, delimiter=delimiter)
                return list(reader)
        except Exception as e:
            raise ValueError(f"Error reading CSV file {file_path}: {e}")
    
    def write_csv_file(self, file_path: Union[str, Path], data: List[Dict[str, Any]], 
                      delimiter: str = ',') -> bool:
        """
        Write data to CSV file
        
        Args:
            file_path: Path to CSV file
            data: List of row dictionaries
            delimiter: CSV delimiter
            
        Returns:
            True if successful
        """
        if not data:
            return False
        
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(file_path, 'w', encoding='utf-8', newline='') as f:
                fieldnames = data[0].keys()
                writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=delimiter)
                writer.writeheader()
                writer.writerows(data)
            return True
        except Exception as e:
            print(f"Error writing CSV file {file_path}: {e}")
            return False
    
    def get_file_info(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Get detailed file information
        
        Args:
            file_path: Path to the file
            
        Returns:
            File information dictionary
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        stat = file_path.stat()
        
        return {
            'name': file_path.name,
            'path': str(file_path.absolute()),
            'size': stat.st_size,
            'size_human': self._human_readable_size(stat.st_size),
            'extension': file_path.suffix.lower(),
            'created': stat.st_ctime,
            'modified': stat.st_mtime,
            'is_file': file_path.is_file(),
            'is_directory': file_path.is_dir(),
            'permissions': oct(stat.st_mode)[-3:],
            'file_type': self._get_file_type(file_path.suffix.lower())
        }
    
    def _human_readable_size(self, size: int) -> str:
        """Convert bytes to human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} PB"
    
    def _get_file_type(self, extension: str) -> str:
        """Determine file type from extension"""
        if extension in self.supported_text_formats:
            return 'text'
        elif extension in self.supported_image_formats:
            return 'image'
        elif extension in self.supported_audio_formats:
            return 'audio'
        elif extension in {'.pdf'}:
            return 'pdf'
        elif extension in {'.docx', '.doc'}:
            return 'word'
        elif extension in {'.xlsx', '.xls'}:
            return 'excel'
        elif extension in {'.pptx', '.ppt'}:
            return 'powerpoint'
        else:
            return 'unknown'
    
    def list_files(self, directory: Union[str, Path], 
                   extensions: Optional[List[str]] = None,
                   recursive: bool = False) -> List[Dict[str, Any]]:
        """
        List files in directory with optional filtering
        
        Args:
            directory: Directory path
            extensions: File extensions to include (e.g., ['.txt', '.pdf'])
            recursive: Search subdirectories
            
        Returns:
            List of file information dictionaries
        """
        directory = Path(directory)
        
        if not directory.exists() or not directory.is_dir():
            raise ValueError(f"Directory not found or not a directory: {directory}")
        
        files = []
        pattern = "**/*" if recursive else "*"
        
        for file_path in directory.glob(pattern):
            if file_path.is_file():
                if extensions is None or file_path.suffix.lower() in extensions:
                    try:
                        file_info = self.get_file_info(file_path)
                        files.append(file_info)
                    except Exception as e:
                        print(f"Error getting info for {file_path}: {e}")
        
        return sorted(files, key=lambda x: x['name'])
    
    def calculate_file_hash(self, file_path: Union[str, Path], algorithm: str = 'md5') -> str:
        """
        Calculate file hash
        
        Args:
            file_path: Path to the file
            algorithm: Hash algorithm ('md5', 'sha1', 'sha256')
            
        Returns:
            File hash as hex string
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        hash_func = getattr(hashlib, algorithm.lower())()
        
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_func.update(chunk)
        
        return hash_func.hexdigest()
    
    def copy_file(self, source: Union[str, Path], destination: Union[str, Path]) -> bool:
        """
        Copy file to destination
        
        Args:
            source: Source file path
            destination: Destination path
            
        Returns:
            True if successful
        """
        try:
            source = Path(source)
            destination = Path(destination)
            
            if not source.exists():
                raise FileNotFoundError(f"Source file not found: {source}")
            
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
            return True
        except Exception as e:
            print(f"Error copying file: {e}")
            return False
    
    def move_file(self, source: Union[str, Path], destination: Union[str, Path]) -> bool:
        """
        Move file to destination
        
        Args:
            source: Source file path
            destination: Destination path
            
        Returns:
            True if successful
        """
        try:
            source = Path(source)
            destination = Path(destination)
            
            if not source.exists():
                raise FileNotFoundError(f"Source file not found: {source}")
            
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(source, destination)
            return True
        except Exception as e:
            print(f"Error moving file: {e}")
            return False
    
    def delete_file(self, file_path: Union[str, Path]) -> bool:
        """
        Delete file
        
        Args:
            file_path: Path to the file
            
        Returns:
            True if successful
        """
        try:
            file_path = Path(file_path)
            if file_path.exists():
                file_path.unlink()
                return True
            return False
        except Exception as e:
            print(f"Error deleting file: {e}")
            return False
    
    def create_directory(self, directory: Union[str, Path]) -> bool:
        """
        Create directory (and parents if needed)
        
        Args:
            directory: Directory path
            
        Returns:
            True if successful
        """
        try:
            Path(directory).mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            print(f"Error creating directory: {e}")
            return False
    
    def batch_process_files(self, directory: Union[str, Path], 
                           extensions: List[str],
                           processor_func,
                           recursive: bool = False) -> List[Dict[str, Any]]:
        """
        Process multiple files with a given function
        
        Args:
            directory: Directory to process
            extensions: File extensions to include
            processor_func: Function to process each file
            recursive: Process subdirectories
            
        Returns:
            List of processing results
        """
        files = self.list_files(directory, extensions, recursive)
        results = []
        
        for file_info in files:
            try:
                result = processor_func(file_info['path'])
                results.append({
                    'file': file_info['path'],
                    'status': 'success',
                    'result': result
                })
            except Exception as e:
                results.append({
                    'file': file_info['path'],
                    'status': 'error',
                    'error': str(e)
                })
        
        return results


if __name__ == "__main__":
    # Example usage
    handler = FileHandler()
    
    # Test directory listing
    try:
        current_dir = Path(".")
        files = handler.list_files(current_dir, extensions=['.py', '.md', '.txt'])
        print(f"Found {len(files)} files in current directory:")
        
        for file_info in files[:5]:  # Show first 5 files
            print(f"- {file_info['name']} ({file_info['size_human']}) - {file_info['file_type']}")
        
        if len(files) > 5:
            print(f"... and {len(files) - 5} more files")
        
    except Exception as e:
        print(f"Error listing files: {e}")
    
    # Test JSON operations
    test_data = {
        "name": "GenerativeAI Starter Kit",
        "version": "1.0.0",
        "components": ["RAG", "Multimodal", "Fine-tuning"],
        "test_run": True
    }
    
    json_file = Path("test_output.json")
    
    # Write JSON
    if handler.write_json_file(json_file, test_data):
        print(f"\n✅ Successfully wrote JSON to {json_file}")
        
        # Read it back
        try:
            loaded_data = handler.read_json_file(json_file)
            print(f"✅ Successfully read JSON: {loaded_data['name']}")
            
            # Clean up
            handler.delete_file(json_file)
            print("✅ Cleaned up test file")
            
        except Exception as e:
            print(f"❌ Error reading JSON: {e}")
    else:
        print("❌ Failed to write JSON file")