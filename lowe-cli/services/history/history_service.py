"""History service for retrieving shell command history."""
import subprocess


class HistoryService:
    """Service for managing and retrieving shell command history."""
    
    @staticmethod
    def get_recent_history(max_lines: int = 100) -> str:
        """
        Run shell history command and return output as a formatted string.
        
        Args:
            max_lines: Maximum number of history lines to retrieve
            
        Returns:
            Formatted string of recent command history
        """
        try:
            result = subprocess.run(
                f"history | tail -r | head -n {max_lines}",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                shell=True,
                executable="/bin/bash"
            )
            
            if result.returncode == 0:
                return "\n".join(
                    line.strip() 
                    for line in result.stdout.splitlines() 
                    if line.strip()
                )
            else:
                return ""
                
        except subprocess.SubprocessError:
            return ""
