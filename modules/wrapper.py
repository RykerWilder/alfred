from langchain_core.tools import tool

def get_tools(net, clock):
    @tool
    def speed_test(input_text: str = "") -> str:
        """Test internet speed and report download and upload speed."""
        return net.execute_speedtest(input_text)

    @tool
    def connection_check(input_text: str = "") -> str:
        """Check whether the internet connection is available."""
        return net.check_connection(input_text)

    @tool
    def play_music(query: str) -> str:
        """Play music on YouTube based on a query."""
        return net.play_music(query)

    @tool
    def web_search(query: str) -> str:
        """Search the web using Google."""
        return net.search(query)

    @tool
    def get_time(input_text: str = "") -> str:
        """Get the current time."""
        return clock.get_time(input_text)

    return [
        speed_test,
        connection_check,
        play_music,
        web_search,
        get_time,
    ]