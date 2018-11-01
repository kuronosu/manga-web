import React, { Component } from 'react'

const MOBILE_VIEW_WIDTH_THRESHOLD = 1000

class MediaQuery extends Component{
  state = {
    shouldShowMobileView: false
  }

  componentDidMount() {
    this.updateResizeStatus()
    addEventListener('resize', this.updateResizeStatus)
  }

  componentWillUnmount() {
    removeEventListener('resize', this.updateResizeStatus)
  }

  updateResizeStatus = () => {
    if (screen.width <= MOBILE_VIEW_WIDTH_THRESHOLD) {
      this.setState({
        shouldShowMobileView: true
      })
    } else {
      this.setState({
        shouldShowMobileView: false
      })
    }
  }

  render() {
    return this.props.children(
      this.state.shouldShowMobileView
    )
  }
}

export default MediaQuery