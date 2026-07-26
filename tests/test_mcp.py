import pytest
from isitreal.mcp_server import mcp


@pytest.mark.asyncio
async def test_mcp_verify_package(mock_pypi):
    res_tuple = await mcp.call_tool("verify_package", {"name": "requests"})
    content, res_dict = res_tuple
    assert res_dict["exists"] is True
    assert res_dict["risk"] == "low"
    assert res_dict["name"] == "requests"


@pytest.mark.asyncio
async def test_mcp_verify_react_codeshift(mock_pypi):
    res_tuple = await mcp.call_tool("verify_package", {"name": "react-codeshift"})
    content, res_dict = res_tuple
    assert res_dict["exists"] is False
    assert res_dict["risk"] == "high"


@pytest.mark.asyncio
async def test_mcp_verify_dependencies(mock_pypi):
    deps_str = "requests>=2.31.0\nreact-codeshift"
    res_tuple = await mcp.call_tool("verify_dependencies", {"file_contents": deps_str})
    content, res_data = res_tuple
    items = res_data if isinstance(res_data, list) else res_data.get("result", [])
    assert len(items) == 2
    assert items[0]["name"] == "react-codeshift"
    assert items[0]["risk"] == "high"
    assert items[1]["name"] == "requests"
    assert items[1]["risk"] == "low"


@pytest.mark.asyncio
async def test_mcp_list_tools():
    tools = await mcp.list_tools()
    tool_names = {t.name for t in tools}
    assert tool_names == {"verify_package", "verify_dependencies"}
