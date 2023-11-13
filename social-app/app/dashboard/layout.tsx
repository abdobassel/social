import {RequireAuth} from '@/components/utils';
import React from "react";

interface Props {
    children: React.ReactNode;
}

export default function Layout({children}: Props) {
    return <RequireAuth>{children}</RequireAuth>;
}
