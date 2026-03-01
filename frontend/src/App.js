import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Layout, Menu } from 'antd';
import { DashboardOutlined, BookOutlined, UserOutlined, LogoutOutlined, FileTextOutlined } from '@ant-design/icons';
import Dashboard from './pages/Dashboard';
import Login from './pages/Login';
import Lancamentos from './pages/Lancamentos';
import Relatorios from './pages/Relatorios';
import Users from './pages/Users';
import './App.css';

const { Header, Content, Footer, Sider } = Layout;

function App() {
    const [collapsed, setCollapsed] = React.useState(false);
    return (
        <Router>
            <Layout style={{ minHeight: '100vh' }}>
                <Sider collapsible collapsed={collapsed} onCollapse={setCollapsed}>
                    <div className="logo" />
                    <Menu theme="dark" mode="inline" defaultSelectedKeys={['1']}>
                        <Menu.Item key="1" icon={<DashboardOutlined />}> Dashboard </Menu.Item>
                        <Menu.Item key="2" icon={<FileTextOutlined />}> Lançamentos </Menu.Item>
                        <Menu.Item key="3" icon={<BookOutlined />}> Relatórios </Menu.Item>
                        <Menu.Item key="4" icon={<UserOutlined />}> Usuários </Menu.Item>
                        <Menu.Item key="5" icon={<LogoutOutlined />}> Logout </Menu.Item>
                    </Menu>
                </Sider>
                <Layout>
                    <Header style={{ background: '#fff', padding: 0 }} />
                    <Content style={{ margin: '0 16px' }}>
                        <Routes>
                            <Route path="/" element={<Dashboard />} />
                            <Route path="/login" element={<Login />} />
                            <Route path="/lancamentos" element={<Lancamentos />} />
                            <Route path="/relatorios" element={<Relatorios />} />
                            <Route path="/users" element={<Users />} />
                        </Routes>
                    </Content>
                    <Footer style={{ textAlign: 'center' }}> Guriata Contabilidade ©2026 </Footer>
                </Layout>
            </Layout>
        </Router>
    );
}

export default App;