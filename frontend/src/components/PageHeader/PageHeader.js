import React from 'react';
import { generateStateID } from '../../components/Info';
import { Link } from 'react-router-dom';
import { Tag } from 'carbon-components-react';
import {
  Header,
  HeaderMenuButton,
  HeaderName,
  SkipToContent,
  SideNav,
  SideNavItems,
  SideNavLink,
  SideNavDivider,
} from 'carbon-components-react/lib/components/UIShell';

import HeaderContainer from 'carbon-components-react/lib/components/UIShell/HeaderContainer';

let config = require('../../config.json');
let states = config['states'];

class PageHeader extends React.Component {
  constructor(props) {
    super();
    this.state = {
      current: 'introduction',
      introduction: true,
    };
  }

  componentDidMount = () => {
    let current_header = window.location.href.split('#/')[1];

    if (!current_header) current_header = 'introduction';

    this.onClickTab(generateStateID(current_header));
  };

  onClickTab = (name, e) => {
    const old = this.state.current;
    const current = name;

    this.setState({
      ...this.state,
      current: current,
      [old]: false,
      [current]: true,
    });
  };

  render() {
    return (
      <HeaderContainer
        render={({ isSideNavExpanded, onClickSideNavExpand }) => (
          <>
            <Header aria-label="Header">
              <SkipToContent />
              <HeaderMenuButton
                onClick={onClickSideNavExpand}
                isActive={!isSideNavExpanded}
                aria-label="Toggle Contents"
              />
              <HeaderName element={Link} to="/" prefix="India">
                COVID-19 Data
              </HeaderName>

              <SideNav
                isFixedNav
                isChildOfHeader
                expanded={!isSideNavExpanded}
                isPersistent={true}
                aria-label="Side navigation">
                <SideNavItems>
                  <SideNavLink
                    large
                    href="/#/introduction"
                    onClick={this.onClickTab.bind(this, 'introduction')}
                    isActive={this.state.introduction}>
                    Introduction
                  </SideNavLink>
                  <SideNavLink
                    large
                    href="/#/contributing"
                    onClick={this.onClickTab.bind(this, 'contributing')}
                    isActive={this.state.contributing}>
                    Contributing
                  </SideNavLink>

                  <SideNavDivider />

                  <SideNavLink
                    large
                    href="/#/analysis"
                    onClick={this.onClickTab.bind(this, 'analysis')}
                    isActive={this.state.analysis}>
                    Inter-State Comparison
                  </SideNavLink>

                  <SideNavDivider />

                  {Object.keys(states).map((key, index) => (
                    <React.Fragment key={index}>
                      <SideNavLink
                        href={'/#/' + generateStateID(states[key]['name'])}
                        onClick={this.onClickTab.bind(
                          this,
                          generateStateID(states[key]['name'])
                        )}
                        isActive={
                          this.state[generateStateID(states[key]['name'])]
                        }>
                        {states[key]['name']}

                        {states[key]['is_complete'] && (
                          <Tag type="blue" className="compressed-tag">
                            {' '}
                            completed{' '}
                          </Tag>
                        )}

                        {!states[key]['is_complete'] && (
                          <Tag type="gray" className="compressed-tag">
                            {' '}
                            in progress{' '}
                          </Tag>
                        )}
                      </SideNavLink>
                    </React.Fragment>
                  ))}
                </SideNavItems>
              </SideNav>
            </Header>
          </>
        )}
      />
    );
  }
}

export default PageHeader;
