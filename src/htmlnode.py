class HTMLNode:
    def __init__(self,tag,value,children,props):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if not self.props:
            return ""
        props_list = list(map(lambda x: f"{x[0]}=\"{x[1]}\"",list(self.props.items())))
        return " " + " ".join(props_list)
    
    def __repr__(self):
        tag = f"Tag: {self.tag}\n"
        value = f"Value: {self.value}\n"
        children = f"Children: {self.children}\n"
        props = f"Props: {self.props_to_html()}"
        return tag+value+children+props

class LeafNode(HTMLNode):
    
    def __init__(self,tag,value,props=None):
        super().__init__(tag,value,None,props)
        if not self.value:
            raise ValueError("All leaf nodes must have a value")

    def to_html(self):
        value = self.value
        props = self.props_to_html()
        open_tag = f"<{self.tag}{props}>" if self.tag else ""
        close_tag = f"</{self.tag}>" if self.tag else ""
        return open_tag + value + close_tag

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)
        if not tag:
            raise ValueError("Tag is required")
        if not children:
            raise ValueError("Children is required")
    def to_html(self):
        children = "".join(list(map(lambda x: x.to_html(),self.children)))
        props = self.props_to_html()
        open_tag = f"<{self.tag}{props}>" if self.tag else ""
        close_tag = f"</{self.tag}>" if self.tag else ""
        return open_tag + children + close_tag
